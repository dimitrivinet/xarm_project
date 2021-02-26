

var recording = false;
var recordButton = document.getElementById("record");
var soundStream;
var mediaRecorder;
var timeslice = 500;

var rec;
var input;

var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext = new AudioContext;

const socket = io('ws://localhost:8000');

socket.on('connect', () => {
  socket.send("connected to server")
});

socket.on('audio_stream_response', stt => {
  console.log(stt);
  document.getElementById("message").innerHTML = stt;
});

const media_constraints = {
  video: false,
  audio: true,
};

const track_constraints = {
  sampleRate: 44100,
  channelCount: 1,
  sampleSize: 16
};

const recorder_options = {
  mimeType: "audio/wave;codecs=pcm"
};

function hasGetUserMedia() {
  return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
}

function startRecordFunc() {

  if (audioContext.state === 'suspended') {
    audioContext.resume();
  }

  console.log("recording");
  recording = true;

  recordButton.innerHTML = "Recording...";

  navigator.mediaDevices.getUserMedia(media_constraints)
    .then(sendStream)
    .catch(function (e) {
      alert('getUserMedia() error: ' + e.name);
      recording = false;
    });
}

function sendStream(stream) {
  console.log("sending stream to server");
  soundStream = stream;

  input = audioContext.createMediaStreamSource(stream);
  // !console.log("debug1");

  rec = new Recorder(input, {
    numChannels: 1
  });
  //start the recording process 
  // !console.log("debug2");
  rec.record();

  // soundStream.getTracks()[0].applyConstraints(track_constraints);
  // console.log(soundStream.getTracks()[0].getConstraints());

  // mediaRecorder = new MediaRecorder(stream, recorder_options);
  // console.log(mediaRecorder.mimeType);
  // mediaRecorder.start();

  // console.log(mediaRecorder.state);
  // console.log("recorder started");

  // mediaRecorder.ondataavailable = function(e) {  
  //   console.log(e.data);  
  //   socket.emit('audio_stream', e.data);
  // }

}

function stopRecordFunc() {
  recordButton.innerHTML = "Record sound!";

  rec.stop();
  rec.exportWAV(function (blob) { 
    console.log(blob.size);
    socket.emit('audio_stream', blob) 
  });

  stopAudioStream(soundStream);
  // mediaRecorder.stop();


  console.log("stopping record");
  socket.send("recording over.")
  recording = false;
}

function stopAudioStream(stream) {
  stream.getTracks().forEach(function (track) {
    if (track.readyState == 'live' && track.kind === 'audio') {
      track.stop();
    }
  });
}

function record() {
  recording ? stopRecordFunc() : startRecordFunc();
}

recordButton.onclick = record;

console.log("begin");

if (hasGetUserMedia()) {
  console.log("Good to go!");
} else {
  alert("getUserMedia() is not supported by your browser");
  console.log("end");
}