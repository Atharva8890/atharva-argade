import React from "react";
import {
  AbsoluteFill,
  interpolate,
  OffthreadVideo,
  staticFile,
  useCurrentFrame,
} from "remotion";
import proc from "../data/footage_proc.json";
import { Theme, mix, withAlpha } from "../lib/sceneTypes";

const CLIPS = (proc as { clips: Record<string, string> }).clips;

/** processed clip for a chapter index, or null */
export const procClip = (i: number): string | null => CLIPS[String(i)] ?? null;

/**
 * Plays a PRE-PROCESSED clip (already slowed + looped + exact length by
 * assets/process_footage.py) linearly at rate 1.0 — fast & robust to render —
 * with a slow Ken Burns move and a cohesive cinematic grade.
 */
export const Footage: React.FC<{ file: string; theme: Theme; dur: number }> = ({
  file,
  theme,
  dur,
}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, dur], [0, 1], { extrapolateRight: "clamp" });
  const scale = interpolate(p, [0, 1], [1.06, 1.16]);
  const panX = interpolate(p, [0, 1], [-1.4, 1.4]);
  const panY = interpolate(p, [0, 1], [1.2, -1.2]);
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <div style={{ position: "absolute", inset: "-6%", transform: `scale(${scale}) translate(${panX}%, ${panY}%)` }}>
        <OffthreadVideo
          src={staticFile(`footage_proc/${file}`)}
          volume={0}
          delayRenderRetries={3}
          delayRenderTimeoutInMilliseconds={120000}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            filter: "contrast(1.14) saturate(0.9) brightness(0.74)",
          }}
        />
      </div>

      {/* palette tint to match the chapter */}
      <AbsoluteFill
        style={{
          background: `linear-gradient(180deg, ${withAlpha(theme.b, 0.35)} 0%, ${withAlpha(
            mix(theme.a, "#000", 0.2),
            0.3
          )} 100%)`,
          mixBlendMode: "soft-light",
        }}
      />
      <AbsoluteFill
        style={{
          background: `radial-gradient(75% 60% at 50% 42%, ${withAlpha(theme.accent, 0.1)} 0%, transparent 60%)`,
          mixBlendMode: "screen",
        }}
      />
      {/* legibility scrim for title cards (top) and captions (bottom) */}
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(180deg, rgba(0,0,0,0.45) 0%, transparent 22%, transparent 55%, rgba(0,0,0,0.78) 100%)",
        }}
      />
    </AbsoluteFill>
  );
};
