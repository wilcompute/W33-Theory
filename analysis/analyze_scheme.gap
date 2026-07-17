LoadPackage("design");
# In standard GAP, we might not have JsonReadFile, so we'll do basic processing.
# We'll write the intersection matrix in a way GAP likes.
f := IO_OpenFile("data/sheet_intersections.json", "r");
s := IO_Read(f);
mat := EvalString(ReplacedString(ReplacedString(s, "[", "["), "]", "]")); # Not quite right, but let's try another way.
