import React from "react";
import Admonition from "@theme/Admonition";

export default function CalloutSolution({ day }) {
  const linkPuzzle = `https://adventofcode.com/2022/day/${day}`;
  const linkGitHub = `https://github.com/kbalston/advent-of-code-2022/tree/main/day${day}`;

  return (
    <Admonition type="info" icon="✅" title="Full solution">
      <p>
        The full solution for <a href={linkPuzzle}>day {day}'s puzzle</a> can be
        found on <a href={linkGitHub}>GitHub</a>.
      </p>
    </Admonition>
  );
}
