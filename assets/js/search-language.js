/* Keep Korean letters in Lunr's index. Loaded before JTD initializes on DOM ready. */
(function (lunr) {
  "use strict";
  if (!lunr) return;

  function unicodeTrimmer(token) {
    return token.update(function (text) {
      return text.replace(/^[^\p{L}\p{N}]+|[^\p{L}\p{N}]+$/gu, "");
    });
  }

  lunr.Pipeline.registerFunction(unicodeTrimmer, "beyondbobUnicodeTrimmer");
  lunr.trimmer = unicodeTrimmer;
})(window.lunr);
