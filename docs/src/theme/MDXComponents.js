import React from "react";
// Import the original mapper
import MDXComponents from "@theme-original/MDXComponents";
import CalloutSolution from "@site/src/components/CalloutSolution";
import CalloutSolutionNotYetAvailable from "@site/src/components/CalloutSolutionNotYetAvailable";
import CalloutWriteup from "@site/src/components/CalloutWriteup";
import CalloutWriteupNotYetAvailable from "@site/src/components/CalloutWriteupNotYetAvailable";

export default {
  // Re-use the default mapping
  ...MDXComponents,
  // Map the following tags to our components as well
  CalloutSolution: CalloutSolution,
  CalloutSolutionNotYetAvailable: CalloutSolutionNotYetAvailable,
  CalloutWriteup: CalloutWriteup,
  CalloutWriteupNotYetAvailable: CalloutWriteupNotYetAvailable,
};
