import React from "react";
import clsx from "clsx";
import styles from "./styles.module.css";

const FeatureList = [
  {
    title: "Solutions in Python",
    // Requires attribution:
    // https://www.flaticon.com/free-icon/planing_4248398?related_id=4248398
    imageSrc: require("@site/static/img/planing.png").default,
    description: (
      <>I'm planning on solving Advent of Code this year primarily in Python.</>
    ),
  },
  {
    title: "Focus on Simplicity",
    // Requires attribution:
    // https://www.flaticon.com/free-icon/website_4248424?related_id=4248424
    imageSrc: require("@site/static/img/website.png").default,
    description: (
      <>
        I'd like my solutions this year to be straightforward and easy to
        understand, favouring simplicity over performance.
      </>
    ),
  },
  {
    title: "Revision-Controlled Development Environment",
    // Requires attribution:
    // https://www.flaticon.com/free-icon/cloud_4248200?related_id=4248200
    imageSrc: require("@site/static/img/cloud.png").default,
    description: (
      <>
        I'm planning to use a revision-controlled{" "}
        <a href="https://containers.dev">devcontainer</a>
        -based development environment.
      </>
    ),
  },
];

function Feature({ imageSrc, title, description }) {
  return (
    <div className={clsx("col col--4")}>
      <div className="text--center padding-vert--md padding-horiz-xl">
        <img src={imageSrc} width="200"></img>
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
