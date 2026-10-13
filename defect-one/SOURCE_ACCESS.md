# Source access and provenance

All authoritative requested inputs were accessible through read-only GitHub
connector actions at their exact pins. None was reconstructed from missing
content. The following were read:

- At 8b350971095fda13884ea568d1914c1edd7fc966: full-slack/THEOREM.md,
  full-slack/DOWNSTREAM.md, full-slack/SOURCES.json, and LICENSE.
- At 06acd4cf46bfe9086f9abc7d85b5c9f171480143: the recovered PROOF.md,
  in particular §§7.2-7.5, plus the needed containment/Gaussian formulas,
  planted prefactor, activity-uniform weighted interface and retained envelope.

The licensed local copies were recovered from the earlier conversation's
mounted handoff ZIP and accepted only after their Git blob hashes matched the
requested pinned source responses or the published source manifest. Source
hashes and byte lengths are in SOURCES.json. The copied documents are unchanged.

The external residual proof was read through the connector. Its SHA-256 is
specified by the published full-slack/SOURCES.json, and its Git blob SHA-1 was
returned by the connector. A full local byte-for-byte rehash of that external
file was not performed. It is an external retained reference rather than a
bundled snapshot because its redistribution license was not established.

A direct raw-HTTPS materialization attempt in the working container failed
because that container had no DNS/network access. Public web opening also did
not provide the pinned pages. These failures did not block access to the
content through the GitHub connector. No conclusions about source correctness
or mathematical novelty follow from those transport failures. The optional
fetch_external_source.py is supplied for a user's independent retrieval; the
new finite checker itself requires no network or external cache.

There was no publication, pull request, message, repository write, or other
external communication. No global current-work or priority determination is
claimed for the new residual estimate.
