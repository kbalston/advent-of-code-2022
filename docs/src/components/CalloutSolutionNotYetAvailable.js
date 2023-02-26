import React from "react";
import Admonition from "@theme/Admonition";

export default function CalloutSolution({ day }) {
  const linkPuzzle = `https://adventofcode.com/2022/day/${day}`;

  return (
    <Admonition type="info" icon="🚧" title="Full solution not yet available">
      <p>
        Unfortunately, my solution for{" "}
        <a href={linkPuzzle}>day {day}'s puzzle</a> is not yet available.
      </p>
    </Admonition>
  );
}
