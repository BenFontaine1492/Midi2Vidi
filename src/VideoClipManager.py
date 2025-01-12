from moviepy.editor import VideoFileClip, concatenate_videoclips


class VideoClipManager:
    """Manages video operations like subclips and concatenation."""
    def __init__(self, video_path):
        self.video = VideoFileClip(video_path)

    def get_clip(self, start_time, duration):
        """Extracts a subclip from the video."""
        return self.video.subclip(start_time, start_time + duration)

    def concatenate_clips(self, clips, output_path):
        """Concatenates and saves the video clips."""
        if clips:
            final_clip = concatenate_videoclips(clips)
            final_clip.write_videofile(output_path)
