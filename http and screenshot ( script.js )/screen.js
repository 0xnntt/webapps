var args = require('system').args;
var page;
var myurl=args[1] 

var renderPage = function (url) {
    page = require('webpage').create();
	page.viewportSize = { width: 1200 ,height: 800};
    page.onNavigationRequested = function(url, type, willNavigate, main) {
        if (main && url!=myurl) {
            myurl = url;
            console.log("redirect caught")
            page.close()
            setTimeout('renderPage(myurl)',1); //Note the setTimeout here
        }
    };

    page.open(url, function(status) {
        if (status==="success") {
            console.log("success")
                page.render(args[2]);
                phantom.exit(0);
        } else {
            console.log("failed")
                phantom.exit(1);
        }
    });
} 

renderPage(myurl);