// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require("prism-react-renderer/themes/github");
const darkCodeTheme = require("prism-react-renderer/themes/dracula");

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "Advent of Code 2022",
  tagline: "Dinosaurs are cool",
  url: "https://kbalston.github.io",
  baseUrl: "/advent-of-code-2022/",
  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",
  // It would be better if this were an ico rather than a png
  favicon: "img/pine-tree-green.png",

  organizationName: "kbalston",
  projectName: "advent-of-code-2022",

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  presets: [
    [
      "classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        pages: {
          path: "src/pages",
        },
        docs: {
          path: "solutions",
          sidebarPath: require.resolve("./sidebars.js"),
          editUrl:
            "https://github.com/kbalston/advent-of-code-2022/tree/main/solutions/",
          routeBasePath: "/",
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      docs: {
        sidebar: {
          hideable: true,
        },
      },
      navbar: {
        title: "Advent of Code 2022",
        logo: {
          alt: "A simple pine tree",
          // https://www.flaticon.com/free-icon/pine-tree_2225518?term=tree&related_id=2225518
          // Requires attribution
          src: "img/pine-tree-green.png",
        },
        items: [
          {
            docId: "about",
            position: "left",
            label: "About",
            to: "/about",
          },
          {
            type: "doc",
            docId: "day1",
            position: "left",
            label: "Solutions",
          },
          {
            href: "https://github.com/kbalston/advent-of-code-2022",
            label: "GitHub",
            position: "right",
          },
        ],
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;
