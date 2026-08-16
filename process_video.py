# in this section we will convert raw video files to text files 
import os 
import subprocess
files = os.listdir("videos")

# print(files)

for file in files:
   
    tutorial_number = file.split("-")[1][0]
    file_name =file.split("-")[0]
   
    print(tutorial_number , file_name)
    subprocess.run([
    "ffmpeg", "-y",
    "-i", f"videos/{file}",
    "-vn",
    "-c:a", "libmp3lame",
    "-b:a", "128k",
    f"audios/{tutorial_number}_{file_name}.mp3"
    ])  
    