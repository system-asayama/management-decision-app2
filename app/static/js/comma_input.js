// Thousand-separator formatting for integer inputs.
// Usage: add class "js-comma-int" to <input type="text">.
// - Formats with commas while typing (caret preserved).
// - On form submit, commas are stripped so the server receives plain digits.

(function () {
  "use strict";

  function normalizeIntString(value) {
    if (value == null) return "";
    let s = String(value);
    // Keep digits and a single leading minus.
    s = s.replace(/[^0-9-]/g, "");
    s = s.replace(/(?!^)-/g, "");
    return s;
  }

  function formatIntString(value) {
    const normalized = normalizeIntString(value);
    if (normalized === "" || normalized === "-") return normalized;

    const negative = normalized.startsWith("-");
    const digits = negative ? normalized.slice(1) : normalized;

    // Remove leading zeros (but keep a single zero).
    const cleanedDigits = digits.replace(/^0+(\d)/, "$1");

    const withCommas = cleanedDigits.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return (negative ? "-" : "") + withCommas;
  }

  function countDigits(text) {
    return (text.match(/\d/g) || []).length;
  }

  function caretPosFromDigitIndex(formatted, digitIndex) {
    if (digitIndex <= 0) return formatted.startsWith("-") ? 1 : 0;

    let pos = 0;
    let seen = 0;
    while (pos < formatted.length) {
      const ch = formatted.charAt(pos);
      if (/\d/.test(ch)) {
        seen += 1;
        if (seen >= digitIndex) {
          return pos + 1;
        }
      }
      pos += 1;
    }
    return formatted.length;
  }

  function formatInputPreserveCaret(input) {
    if (!input) return;
    const raw = input.value;

    const start = input.selectionStart ?? raw.length;
    const beforeCaret = raw.slice(0, start);
    const digitIndex = countDigits(beforeCaret);

    const formatted = formatIntString(raw);
    input.value = formatted;

    const newPos = caretPosFromDigitIndex(formatted, digitIndex);
    try {
      input.setSelectionRange(newPos, newPos);
    } catch (_) {
      // Some input types may not support selection ranges.
    }
  }

  function stripCommas(value) {
    if (value == null) return value;
    return String(value).replace(/,/g, "");
  }

  function attach() {
    const inputs = Array.from(document.querySelectorAll("input.js-comma-int"));

    // Initial format for edit screens
    inputs.forEach((input) => {
      input.value = formatIntString(input.value);

      input.addEventListener("input", function () {
        formatInputPreserveCaret(input);
      });

      // If user pastes something, normalize on blur too.
      input.addEventListener("blur", function () {
        input.value = formatIntString(input.value);
      });
    });

    // Strip commas just before submit
    const forms = new Set(inputs.map((i) => i.form).filter(Boolean));
    forms.forEach((form) => {
      // Use capture phase so this runs before other submit handlers (including ones that do fetch + preventDefault).
      form.addEventListener(
        "submit",
        function () {
        inputs
          .filter((i) => i.form === form)
          .forEach((i) => {
            i.value = stripCommas(i.value);
          });
        },
        true
      );
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", attach);
  } else {
    attach();
  }
})();
