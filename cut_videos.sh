IN_DATA_DIR="./videos"
OUT_DATA_DIR="./video_crop"
if [[ ! -d "${OUT_DATA_DIR}" ]]; then
  echo "${OUT_DATA_DIR} doesn't exist. Creating it.";
  mkdir -p ${OUT_DATA_DIR}
fi
ffmpeg -ss 10 -t 11 -y -i "${IN_DATA_DIR}/A.mp4" "${OUT_DATA_DIR}/A.mp4"
ffmpeg -ss 20 -t 11 -y -i "${IN_DATA_DIR}/A.mp4" "${OUT_DATA_DIR}/B.mp4"
ffmpeg -ss 30 -t 11 -y -i "${IN_DATA_DIR}/A.mp4" "${OUT_DATA_DIR}/C.mp4"
