import React from "react";
import {
  AbsoluteFill,
  interpolate,
  Loop,
  OffthreadVideo,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import footage from "../data/footage.json";
import { Theme, mix, withAlpha } from "../lib/sceneTypes";

type Clip = { file: string; duration: number; startFrom: number };
const BY = (footage as { byChapter: Record<string, Clip> }).byChapter;

export const hasFootage = (key: string) => Boolean(BY[key]);

const PLAYBACK = 0.62; // cinematic slow-motion

/** one looped iteration: graded video + slow Ken Burns */
const ClipShot: React.FC<{ clip: Clip; theme: Theme; loopFrames: number }> = ({
  clip,
  theme,
  loopFrames,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = frame / loopFrames;
  const scale = interpolate(p, [0, 1], [1.08, 1.2]);
  const panX = interpolate(p, [0, 1], [-1.5, 1.5]);
  const panY = interpolate(p, [0, 1], [1.5, -1.5]);
  return (
    <AbsoluteFill>
      <div
        style={{
          position: "absolute",
          inset: "-6%",
          transform: `scale(${scale}) translate(${panX}%, ${panY}%)`,
        }}
      >
        <OffthreadVideo
          src={staticFile(`footage/${clip.file}`)}
          startFrom={Math.round(clip.startFrom * fps)}
          playbackRate={PLAYBACK}
          volume={0}
          // graded for a cohesive, cinematic, slightly teal-orange look
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            filter: "contrast(1.14) saturate(0.9) brightness(0.74)",
          }}
        />
      </div>
    </AbsoluteFill>
  );
};

export const Footage: React.FC<{ chapterKey: string; theme: Theme }> = ({
  chapterKey,
  theme,
}) => {
  const { fps } = useVideoConfig();
  const clip = BY[chapterKey];
  if (!clip) return null;
  const content = Math.max(2, clip.duration - clip.startFrom);
  const loopFrames = Math.max(30, Math.round((content / PLAYBACK) * fps));

  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <Loop durationInFrames={loopFrames}>
        <ClipShot clip={clip} theme={theme} loopFrames={loopFrames} />
      </Loop>

      {/* colour-grade tint to match the chapter palette */}
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
      {/* legibility scrim: darken top (title cards) and bottom (captions) */}
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(180deg, rgba(0,0,0,0.45) 0%, transparent 22%, transparent 55%, rgba(0,0,0,0.78) 100%)",
        }}
      />
    </AbsoluteFill>
  );
};
