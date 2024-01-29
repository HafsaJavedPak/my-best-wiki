const root = document.documentElement;
var cssVariable = getComputedStyle(root).getPropertyValue('--my-variable');

var element = document.getElementById("mini-banner");
var bannerHeight = element.offsetHeight;

// Set a CSS variable with the calculated height
document.documentElement.style.setProperty("--bannerHeight", bannerHeight + "px");
