INPUT_DIRECTORY=/home/christopher/musicpy/MusicPy

# TFRecord file that will contain NoteSequence protocol buffers.
SEQUENCES_TFRECORD=/tmp/notesequences.tfrecord

convert_dir_to_note_sequences \
  --input_dir="/home/christopher/musicpy/MusicPy" \
  --output_file="/tmp/notesequences.tfrecord" \
  --recursive

python /home/christopher/anaconda3/envs/magenta/lib/python3.7/site-packages/magenta/scripts/convert_dir_to_note_sequences.py \
    --input_dir="/home/christopher/musicpy/MusicPy" \
    --output_file="/tmp/notesequences.tfrecord" \
    --log=INFO