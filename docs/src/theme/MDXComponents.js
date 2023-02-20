import React from "react";
// Import the original mapper
import MDXComponents from "@theme-original/MDXComponents";
import CalloutSolution from "@site/src/components/CalloutSolution";

export default {
  // Re-use the default mapping
  ...MDXComponents,
  // Map the following tags to our components as well
  CalloutSolution: CalloutSolution,
};
