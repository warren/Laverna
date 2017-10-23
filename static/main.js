$(window).on("load", function() {
    $("#loading-cover").fadeOut(500);
});

$(document).ready(function()
{
    var socket = io.connect("http://" + document.domain + ":" + location.port);
    var usersQueued = 0;

    socket.on("connect", function()
    {
        socket.emit("joined", {});
        console.log("A user just accessed the site.");
    });

    socket.on("addTally", function(data)
    {
        //$("#tallyIcons").append('<i class="fa ' + data.iconName + '"></i>');
        // data.iconName is a string containing the name of the chosen fa-icon
        usersQueued = usersQueued + 1;

        console.log("Tally with id " + data.iconName + "added. There are now " + usersQueued + " users queued.");

        if (usersQueued == 1)
        {
            $("#user-count-subtext").text("There is currently 1 user in the queue.");
        } else {
            $("#user-count-subtext").text("There are currently " + usersQueued + " users in the queue.");
        }
    });

    socket.on("removeTally", function(data)
    {
        //$("i:." + data.iconName, "#tallyIcons").remove();
        // Removes all i elements of tallyIcons that have the class name iconName
        usersQueued = usersQueued - 1;

        console.log("Tally with id " + data.iconName + "removed. There are now " + usersQueued + " users queued.");

        if (usersQueued == 1)
        {
            $("#user-count-subtext").text("There is currently 1 user in the queue.");
        } else {
            $("#user-count-subtext").text("There are currently " + usersQueued + " users in the queue.");
        }
    });

    socket.on("setup", function(data)
    {
        setupTallies(data.iconList);
        setupTimer(data.seconds);
        console.log("Time left is " + Math.floor(data.seconds));
        setupPhoneNumber(data.magicNumber);
        console.log("Magic number is " + data.magicNumber);
        setupUniqueUsers(data.uniqueUsers);
        console.log(data.uniqueUsers + " unique users set up.");
    });

    socket.on("resetTallies", function()
    {
        //$("#tallyIcons").empty();
        usersQueued = 0;
        $("#user-count-subtext").text("There are currently 0 users in the queue.");
        console.log("Tallies reset!");
    });

    socket.on("setUniqueUsers", function(data)
    {
        setupUniqueUsers(data.uniqueUsers);
    });

    //open the lateral panel
    $(".cd-btn").on("click", function(event){
        event.preventDefault();
        $('.cd-panel').addClass('is-visible');
    });
    //close the lateral panel
    $('.cd-panel').on('click', function(event){
        if( $(event.target).is('.cd-panel') || $(event.target).is('.cd-panel-close') ) {
            $('.cd-panel').removeClass('is-visible');
            event.preventDefault();
        }
    });
});

function setupTallies(iconList)
{
    usersQueued = iconList.length;

    /*for(i=0; i<usersQueued; i++)
    {
        $("#tallyIcons").append('<i class="fa ' + iconList[i] + '"></i>');
    };*/

    if (usersQueued == 1)
    {
        $("#user-count-subtext").text("There is currently 1 user in the queue.");
    } else {
        $("#user-count-subtext").text("There are currently " + usersQueued + " users in the queue.");
    }

    console.log("Tallies set up!");
}

function setupTimer(secondsLeft)
{
    var nowDate = new Date().getTime();
    // This is the # of milliseconds since Jan 1 1970 00:00:00
    var countdownDate = new Date(nowDate + (secondsLeft * 1000)).getTime();
    // This constructs a countdown date ahead of our current time by (secondsLeft * 100) milliseconds

    var countdownInterval = setInterval(function()
    {
        var nowDate = new Date().getTime();
        var distance = countdownDate - nowDate;
        console.log("distance is " + distance);

        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        $("#timer-subtext").text("and the next round will begin in " + hours + " hours, " + minutes + " minutes, and " + seconds + " seconds.");
        if (distance <= 1000)
        {
            clearInterval(countdownInterval);
            var socket = io.connect("http://" + document.domain + ":" + location.port);
            socket.emit("joined", {});
        }
    }, 1000);
}

function setupPhoneNumber(magicNumber)
{
    magicNumber = magicNumber.replace(/[^\d]/g, "");
    // Removes all characters that aren't 0-9 from the string
    magicNumber = magicNumber.substr(1);
    // Removes the first character, which will be the 1 from the US dialing code

    if (magicNumber.length == 10)
    {
        magicNumber = magicNumber.replace(/(\d{3})(\d{3})(\d{4})/, "($1) $2-$3");
        // Formats the 10-digit number into the form (xxx) yyy-zzzz
    } else
    {
        console.log("ERROR: Magic number could not be formatted. Check your tokens file.");
    }

    $("#phone-number-subtext").text("The magic number is " + magicNumber + ",");
}

function setupUniqueUsers(uniqueUsers)
{
    $(".unique-users").text("Number of unique users who have texted the number: " + uniqueUsers);
}
