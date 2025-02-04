const chalk = require("chalk");
const config = require("./Config");

/**
 * Colorize a string with Chalk
 * @param str string to colorize
 * @param color color to use (see Chalk documentation)
 * @returns {*} colorized string for console output
 */
function colored(str, color) {
  return config.colors ? chalk[color](str) : str;
}

/**
 * Check if a string is a valid JSON
 * @param str string to check
 * @returns {boolean} true if string is a valid JSON, false otherwise
 */
function isValidJSON(str) {
  try {
    JSON.parse(str);
    return true;
  } catch (e) {
    if (config.debug) console.error(e);
    return false;
  }
}

module.exports = { colored, isValidJSON };
