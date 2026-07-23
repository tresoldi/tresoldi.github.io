-- Convert Pandoc footnotes into Tufte-style sidenotes/marginnotes.
--
--   [^1]  ...text...        -> numbered sidenote in the right margin
--
-- The generated markup follows the tufte-css convention: a numbered label,
-- a hidden checkbox (so notes toggle inline on narrow screens without JS),
-- and the note content. Numbering is handled in CSS via counters.

local counter = 0

function Note(el)
  counter = counter + 1
  local id = "sn-" .. counter

  -- Render the note's block content, then unwrap a single leading paragraph
  -- so the note sits inline inside a <span>.
  local inner = pandoc.write(pandoc.Pandoc(el.content), "html")
  inner = inner:gsub("^%s*<p>(.-)</p>%s*$", "%1")

  local raw = table.concat({
    '<label for="', id, '" class="margin-toggle sidenote-number"></label>',
    '<input type="checkbox" id="', id, '" class="margin-toggle"/>',
    '<span class="sidenote">', inner, '</span>',
  })

  return pandoc.RawInline("html", raw)
end
