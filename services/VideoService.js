import { authApi, noAuthApi } from "./api";
import { endPoints } from "./resources";

/**
 * VideoService is responsible for editing videos.
 */

export class VideoService {
  static async uploadVideo(videoFile, fromLang, toLang, action) {
    try {
      const data = await authApi.post(
        endPoints.videoUpload +
          `?from_lang=${fromLang}&to_lang=${toLang}&action=${action}`,
        fromLang,
        toLang,
        action,
        videoFile
      );
      console.log(data, "data");
      return data;
    } catch (error) {
      console.log(error, "caught error");
    }
  }

  static async getLanguages() {
    try {
      const data = await noAuthApi.get(endPoints.languages);
      return data;
    } catch (error) {
      console.log(error, "caught error");
    }
  }

  static async getCaptions() {
    try {
      const data = await authApi.get(endPoints.getSubtitle);
      console.log(data, "data");
      return data;
    } catch (error) {
      console.log(error, "caught error");
    }
  }
}
