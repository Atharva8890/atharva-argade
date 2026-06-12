import React from "react";
import { AbsoluteFill, Audio, staticFile } from "remotion";
import { timeline } from "./lib/timeline";
import { Background } from "./components/Background";
import { ChapterTitles } from "./components/ChapterTitles";
import { Captions } from "./components/Captions";
import { EndCard } from "./components/EndCard";
import {
  CameraShake,
  Fades,
  FilmHUD,
  Grain,
  Letterbox,
  LightLeak,
  Vignette,
} from "./components/Overlays";

export const Documentary: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <Audio src={staticFile(timeline.audio)} />

      {/* moving image + title cards live inside the handheld camera */}
      <CameraShake>
        <Background />
        <ChapterTitles />
        <EndCard />
      </CameraShake>

      {/* captions stay rock-steady for readability */}
      <Captions />

      {/* graded cinematic finish */}
      <LightLeak />
      <Grain />
      <Vignette />
      <FilmHUD />
      <Letterbox />
      <Fades />
    </AbsoluteFill>
  );
};
