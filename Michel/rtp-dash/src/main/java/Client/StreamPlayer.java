package Client;

import uk.co.caprica.vlcj.component.EmbeddedMediaPlayerComponent;

import javax.swing.*;

public class StreamPlayer {

    /**
     * @param args the command line arguments
     */
    private final JFrame frame;
    private final EmbeddedMediaPlayerComponent mediaPlayerComponent;
    private float lostFrames=0;
    private float i_lost_pictures;


    public StreamPlayer(String dst){
        frame =new JFrame("Test Media Player");
        frame.setBounds(100, 100, 1280, 720);
        mediaPlayerComponent = new EmbeddedMediaPlayerComponent();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setContentPane(mediaPlayerComponent);
        frame.setVisible(true);
        String[] options = {":sout=#transcode{vcodec=mp4v,vb=4096,scale=1,acodec=mp4a,ab=128,channels=2,samplerate=44100}:duplicate{dst=file{dst=" + dst + "},dst=display}"};
        mediaPlayerComponent.getMediaPlayer().playMedia("rtsp://192.168.0.121:8554/:tame_impala.mp4", options);

    }

}


