from BaseEnv import BaseEnv

class ArtificialIntelligenceMachineLearning(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.generated_images = []
        self.generated_videos = []
        self.speech_outputs = []
        self.edited_images = []

    def midjourney_create_image(
        self,
        *,
        prompt,
        style_version="V6",
        aspect_ratio="1:1",
        quality=1.0,
        style_params=None
    ):
        if not isinstance(prompt, str) or not prompt.strip():
            return {"success": False, "message": "Prompt must be a non-empty string."}
        if style_version not in ["V5", "V6", "niji"]:
            return {"success": False, "message": "Invalid style_version."}
        try:
            quality = float(quality)
        except Exception:
            return {"success": False, "message": "Quality must be a number."}
        if not (0.25 <= quality <= 2.0):
            return {"success": False, "message": "Quality must be between 0.25 and 2.0."}
        image_set = {
            "prompt": prompt,
            "style_version": style_version,
            "aspect_ratio": aspect_ratio,
            "quality": quality,
            "style_params": style_params if style_params is not None else {},
            "images": [f"midjourney_image_{len(self.generated_images)}_{i+1}.png" for i in range(4)]
        }
        self.generated_images.append(image_set)
        return {
            "success": True,
            "data": {
                "images": image_set["images"],
                "info": {
                    "prompt": prompt,
                    "style_version": style_version,
                    "aspect_ratio": aspect_ratio,
                    "quality": quality,
                    "style_params": style_params if style_params is not None else {}
                }
            }
        }

    def stable_diffusion_generate(
        self,
        *,
        prompt,
        negative_prompt,
        seed,
        model="sd_xl_base_1.0",
        steps=50,
        cfg_scale=7.5,
        width=1024,
        height=1024,
        sampler="DPM++ 2M Karras"
    ):
        if not isinstance(prompt, str) or not prompt.strip():
            return {"success": False, "message": "Prompt must be a non-empty string."}
        if not isinstance(negative_prompt, str):
            return {"success": False, "message": "negative_prompt must be a string."}
        try:
            seed = int(seed)
        except Exception:
            return {"success": False, "message": "Seed must be an integer."}
        try:
            steps = int(steps)
        except Exception:
            return {"success": False, "message": "Steps must be an integer."}
        if not (1 <= steps <= 150):
            return {"success": False, "message": "Steps must be between 1 and 150."}
        try:
            cfg_scale = float(cfg_scale)
        except Exception:
            return {"success": False, "message": "cfg_scale must be a number."}
        if not (1 <= cfg_scale <= 30):
            return {"success": False, "message": "cfg_scale must be between 1 and 30."}
        try:
            width = int(width)
            height = int(height)
        except Exception:
            return {"success": False, "message": "Width and height must be integers."}
        image = f"stable_diffusion_image_{len(self.generated_images)+1}.png"
        image_info = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "seed": seed,
            "model": model,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "width": width,
            "height": height,
            "sampler": sampler,
            "image": image
        }
        self.generated_images.append(image_info)
        return {
            "success": True,
            "data": {
                "image": image,
                "info": image_info
            }
        }

    def runway_generate_video(
        self,
        *,
        prompt,
        num_frames,
        seed,
        mode="text_to_video",
        duration=4.0,
        fps=24,
        style_preset="cinematic",
        motion_bucket_id=127
    ):
        if not isinstance(prompt, str) or not prompt.strip():
            return {"success": False, "message": "Prompt must be a non-empty string."}
        try:
            num_frames = int(num_frames)
        except Exception:
            return {"success": False, "message": "num_frames must be an integer."}
        try:
            seed = int(seed)
        except Exception:
            return {"success": False, "message": "seed must be an integer."}
        if mode not in ["text_to_video", "image_to_video", "video_to_video"]:
            return {"success": False, "message": "Invalid mode."}
        try:
            duration = float(duration)
        except Exception:
            return {"success": False, "message": "duration must be a number."}
        if not (1 <= duration <= 18):
            return {"success": False, "message": "duration must be between 1 and 18."}
        if fps not in [24, 30]:
            return {"success": False, "message": "fps must be 24 or 30."}
        try:
            motion_bucket_id = int(motion_bucket_id)
        except Exception:
            return {"success": False, "message": "motion_bucket_id must be an integer."}
        if not (1 <= motion_bucket_id <= 255):
            return {"success": False, "message": "motion_bucket_id must be between 1 and 255."}
        video = f"runway_video_{len(self.generated_videos)+1}.mp4"
        video_info = {
            "prompt": prompt,
            "mode": mode,
            "duration": duration,
            "fps": fps,
            "style_preset": style_preset,
            "num_frames": num_frames,
            "motion_bucket_id": motion_bucket_id,
            "seed": seed,
            "video": video
        }
        self.generated_videos.append(video_info)
        return {
            "success": True,
            "data": {
                "video": video,
                "info": video_info
            }
        }

    def elevenlabs_text_to_speech(
        self,
        *,
        text,
        voice_id="josh",
        model="eleven_multilingual_v2",
        stability=0.5,
        similarity_boost=0.75,
        style=0.0,
        use_speaker_boost=True
    ):
        if not isinstance(text, str) or not text.strip():
            return {"success": False, "message": "Text must be a non-empty string."}
        if len(text) > 2500:
            return {"success": False, "message": "Text exceeds maximum length of 2500 characters."}
        try:
            stability = float(stability)
            similarity_boost = float(similarity_boost)
            style = float(style)
        except Exception:
            return {"success": False, "message": "stability, similarity_boost, and style must be numbers."}
        if not (0 <= stability <= 1):
            return {"success": False, "message": "stability must be between 0 and 1."}
        if not (0 <= similarity_boost <= 1):
            return {"success": False, "message": "similarity_boost must be between 0 and 1."}
        if not (0 <= style <= 1):
            return {"success": False, "message": "style must be between 0 and 1."}
        speech = f"speech_{len(self.speech_outputs)+1}.mp3"
        speech_info = {
            "text": text,
            "voice_id": voice_id,
            "model": model,
            "stability": stability,
            "similarity_boost": similarity_boost,
            "style": style,
            "use_speaker_boost": bool(use_speaker_boost),
            "speech": speech
        }
        self.speech_outputs.append(speech_info)
        return {
            "success": True,
            "data": {
                "audio": speech,
                "info": speech_info
            }
        }

    def dalle_edit_image(
        self,
        *,
        image_url,
        prompt,
        mask_url=None,
        size="1024x1024",
        quality="standard",
        model="dall-e-3",
        n=1
    ):
        if not isinstance(image_url, str) or not image_url.strip():
            return {"success": False, "message": "image_url must be a non-empty string."}
        if not isinstance(prompt, str) or not prompt.strip():
            return {"success": False, "message": "prompt must be a non-empty string."}
        if size not in ["1024x1024", "1024x1792", "1792x1024"]:
            return {"success": False, "message": "Invalid size."}
        if quality not in ["standard", "hd"]:
            return {"success": False, "message": "Invalid quality."}
        if model not in ["dall-e-2", "dall-e-3"]:
            return {"success": False, "message": "Invalid model."}
        try:
            n = int(n)
        except Exception:
            return {"success": False, "message": "n must be an integer."}
        if not (1 <= n <= 4):
            return {"success": False, "message": "n must be between 1 and 4."}
        images = [f"dalle_edit_image_{len(self.edited_images)+1}_{i+1}.png" for i in range(n)]
        edit_info = {
            "image_url": image_url,
            "prompt": prompt,
            "mask_url": mask_url,
            "size": size,
            "quality": quality,
            "model": model,
            "n": n,
            "images": images
        }
        self.edited_images.append(edit_info)
        return {
            "success": True,
            "data": {
                "images": images,
                "info": edit_info
            }
        }

    def stability_edit_image(
        self,
        *,
        image_url,
        prompt,
        edit_mode="img2img",
        control_mode=None,
        strength=0.75,
        guidance_scale=7.5,
        seed=None,
        steps=30,
        control_guidance=1.0
    ):
        if not isinstance(image_url, str) or not image_url.strip():
            return {"success": False, "message": "image_url must be a non-empty string."}
        if not isinstance(prompt, str) or not prompt.strip():
            return {"success": False, "message": "prompt must be a non-empty string."}
        if edit_mode not in ["img2img", "inpaint", "controlnet"]:
            return {"success": False, "message": "Invalid edit_mode."}
        if edit_mode == "controlnet":
            if control_mode not in ["canny", "depth", "pose", "seg", "hed", "scribble", "normal"]:
                return {"success": False, "message": "Invalid control_mode for controlnet."}
        try:
            strength = float(strength)
            guidance_scale = float(guidance_scale)
            control_guidance = float(control_guidance)
        except Exception:
            return {"success": False, "message": "strength, guidance_scale, and control_guidance must be numbers."}
        if not (0 <= strength <= 1):
            return {"success": False, "message": "strength must be between 0 and 1."}
        if not (1 <= guidance_scale <= 20):
            return {"success": False, "message": "guidance_scale must be between 1 and 20."}
        if not (0 <= control_guidance <= 2):
            return {"success": False, "message": "control_guidance must be between 0 and 2."}
        if seed is not None:
            try:
                seed = int(seed)
            except Exception:
                return {"success": False, "message": "seed must be an integer or null."}
        try:
            steps = int(steps)
        except Exception:
            return {"success": False, "message": "steps must be an integer."}
        if not (10 <= steps <= 150):
            return {"success": False, "message": "steps must be between 10 and 150."}
        image = f"stability_edit_image_{len(self.edited_images)+1}.png"
        edit_info = {
            "image_url": image_url,
            "prompt": prompt,
            "edit_mode": edit_mode,
            "control_mode": control_mode,
            "strength": strength,
            "guidance_scale": guidance_scale,
            "seed": seed,
            "steps": steps,
            "control_guidance": control_guidance,
            "image": image
        }
        self.edited_images.append(edit_info)
        return {
            "success": True,
            "data": {
                "image": image,
                "info": edit_info
            }
        }