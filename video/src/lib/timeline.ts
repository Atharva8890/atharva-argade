import data from "../data/timeline.json";

export type Theme = { a: string; b: string; accent: string };

export type Word = { w: string; emph: boolean; s: number; e: number };

export type Caption = {
  chapter: string;
  kind: string;
  start: number;
  end: number;
  words: Word[];
  lines: [number, number][];
};

export type Chapter = {
  key: string;
  num: number;
  kind: "hook" | "title" | "chapter" | "finale" | "endcard";
  title: string;
  kicker: string;
  scene: "skyline" | "stars" | "grid" | "timeline" | "map" | "flare" | "dark";
  theme: Theme;
  start: number;
  end: number;
  cardAt?: number;
};

export type Timeline = {
  fps: number;
  width: number;
  height: number;
  totalSeconds: number;
  durationInFrames: number;
  audio: string;
  chapters: Chapter[];
  captions: Caption[];
};

export const timeline = data as unknown as Timeline;

export const FPS = timeline.fps;

export const sec = (s: number) => s * FPS;

/** total chapters that are "real" numbered chapters (for HUD) */
export const TOTAL_CHAPTERS = Math.max(
  ...timeline.chapters.filter((c) => c.kind === "chapter").map((c) => c.num),
  1
);

export function chapterAt(t: number): Chapter {
  let cur = timeline.chapters[0];
  for (const c of timeline.chapters) {
    if (t >= c.start) cur = c;
  }
  return cur;
}

export function captionAt(t: number): Caption | null {
  for (const c of timeline.captions) {
    if (t >= c.start && t <= c.end + 0.25) return c;
  }
  return null;
}
