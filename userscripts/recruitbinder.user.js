// ==UserScript==
// @name         Accelerator KeyBinder
// @namespace    HN67
// @version      0.1
// @description  Accelerator keybinds
// @author       HN67
// @downloadURL  https://github.com/HN67/scripts/raw/master/userscripts/recruitbinder.user.js
// @match        https://10000islands.net/*
// @require      https://craig.global.ssl.fastly.net/js/mousetrap/mousetrap.min.js?a4098
// @grant        none
// ==/UserScript==

/* global Mousetrap */

(function() {
    'use strict';

    // recruit nation
    Mousetrap.bind("z", function(event) {
        let button = document.querySelector("input[value='Recruit']");
        button.click();
    });

    // delete nation
    Mousetrap.bind("x", function(event) {
        let button = document.querySelector("input[value='remove unsuitable nation']");
        button.click();
    });

    // next nation
    Mousetrap.bind("c", function(event) {
        let button = document.getElementById("clean");
        button.click();
    });

    // age in MILLISECONDS
    const SCRAP_AGE = 30 * 60 * 1000;

    // filtered delete nation
    // only deletes if at least as old as scrap age
    Mousetrap.bind("s", function(event) {
        let cRow = document.querySelectorAll("#updateData tr")[1];
        if (cRow.children[0].textContent !== "Creation") {
            console.log("Scraping mismatch");
            return;
        }
        let delta = Date.now() - Date.parse(cRow.children[1].textContent);
        if (delta >= SCRAP_AGE) {
            let button = document.querySelector("input[value='remove unsuitable nation']");
            button.click();
        }
    });

})();
