import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { captionAt, chapterAt } from "../lib/timeline";
import { inter } from "../theme";
import { mix, withAlpha } from "../lib/sceneTypes";

const INK = "#f7f5ef";

export const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const cap = captionAt(t);
  if (!cap || cap.words.length === 0) return null;

  const accent = chapterAt(t).theme.accent;

  // active word = last word whose start has passed
  let activeIdx = 0;
  for (let i = 0; i < cap.words.length; i++) {
    if (cap.words[i].s <= t) activeIdx = i;
  }
  if (t < cap.words[0].s) activeIdx = 0;

  // pick the line containing the active word
  let line = cap.lines.find(([a, b]) => activeIdx >= a && activeIdx < b) ?? cap.lines[0];
  const [a, b] = line;
  const words = cap.words.slice(a, b);

  // line entrance (slide/blur in when it appears)
  const lineStart = cap.words[a].s;
  const intro = interpolate(t - lineStart, [-0.05, 0.22], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const outro = interpolate(t, [cap.end + 0.05, cap.end + 0.28], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const vis = Math.min(intro, outro);

  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: "13%" }}>
      <div
        style={{
          maxWidth: "82%",
          textAlign: "center",
          fontFamily: inter,
          fontWeight: 800,
          fontSize: 62,
          lineHeight: 1.18,
          letterSpacing: 0.3,
          opacity: vis,
          transform: `translateY(${(1 - intro) * 26}px)`,
          filter: `blur(${(1 - intro) * 6}px)`,
        }}
      >
        {words.map((w, i) => {
          const gi = a + i;
          const spoken = t >= w.e;
          const active = t >= w.s && t < w.e;
          const reveal = interpolate(t - w.s, [-0.02, 0.16], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          let color = "rgba(255,255,255,0.34)"; // upcoming
          if (spoken) color = w.emph ? mix(accent, "#ffffff", 0.25) : INK;
          if (active) color = mix(accent, "#ffffff", 0.15);
          const scale = active ? 1.0 + 0.12 * reveal : spoken ? 1 : 0.98;
          const lift = active ? -6 * reveal : 0;
          const glow = active || (spoken && w.emph)
            ? `0 0 26px ${withAlpha(accent, 0.65)}, 0 4px 18px rgba(0,0,0,0.6)`
            : "0 3px 16px rgba(0,0,0,0.65)";
          return (
            <span
              key={gi}
              style={{
                display: "inline-block",
                margin: "0 0.22em",
                color,
                textTransform: w.emph ? "uppercase" : "none",
                transform: `translateY(${lift}px) scale(${scale})`,
                textShadow: glow,
                transition: "none",
              }}
            >
              {w.w}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
