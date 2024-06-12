from rest_framework import generics, permissions
from .models import Video
from .serializers import VideoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import StreamingHttpResponse
import cv2
import threading
import queue

class VideoListCreate(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter videos based on the current authenticated user
        return Video.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VideoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = get_object_or_404(Video, pk=self.kwargs['pk'], user=self.request.user)
        return obj

# OpenCV video streaming
class VideoStreamHandler:
    def __init__(self, video_url):
        self.video_url = video_url
        self.stream = cv2.VideoCapture(video_url)
        self.stopped = False
        self.frame_queue = queue.Queue()

    def start(self):
        threading.Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while not self.stopped:
            if not self.frame_queue.full():
                ret, frame = self.stream.read()
                if not ret:
                    self.stop()
                    return
                self.frame_queue.put(frame)

    def read(self):
        return self.frame_queue.get()

    def stop(self):
        self.stopped = True
        self.stream.release()

def generate_frames(video_url):
    vs = VideoStreamHandler(video_url).start()
    while True:
        frame = vs.read()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@api_view(['GET'])
def video_stream(request, pk):
    video = get_object_or_404(Video, pk=pk)
    return StreamingHttpResponse(generate_frames(video.video_url), content_type='multipart/x-mixed-replace; boundary=frame')
