import React from "react";
import Admonition from "@theme/Admonition";

export default function CalloutSolution({ day }) {
  return (
    <Admonition type="info" icon="✅" title="Full solution">
      <p>
        The full solution for this day's puzzle can be found on{" "}
        <a
          href={
            "https://github.com/kbalston/advent-of-code-2022/tree/main/day" +
            day
          }
        >
          GitHub
        </a>
        .
      </p>
    </Admonition>
  );
}
