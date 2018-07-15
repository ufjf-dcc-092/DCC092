package DashConverter;

import com.xuggle.mediatool.IMediaReader;
import com.xuggle.mediatool.IMediaWriter;
import com.xuggle.mediatool.ToolFactory;
import com.xuggle.xuggler.IContainer;
import com.xuggle.xuggler.IContainerFormat;

import javax.xml.parsers.*;
import javax.xml.transform.*;
import javax.xml.transform.dom.*;
import javax.xml.transform.stream.*;
import org.xml.sax.*;
import org.w3c.dom.*;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.util.ArrayList;
import java.util.regex.Pattern;

import static com.xuggle.xuggler.ICodec.ID.CODEC_ID_H264;
import static com.xuggle.xuggler.ICodec.ID.CODEC_ID_MP3;

class Representation {

    public String resolution;
    public int numberOfSeguiments;

    public Representation(String resolution, int numberOfSeguiments){
        this.resolution = resolution;
        this.numberOfSeguiments = numberOfSeguiments;
    }
}



public class DashConverter {

    private byte[] buffer = new byte[1024];
    private FileInputStream inputStream;
    private String mp4Src;
    private String mp4Dst;
    private String fileName;
    private String fileExtension;
    private ArrayList<Representation> resolutions = new ArrayList<Representation>();

    public DashConverter(String mp4Src, String mp4Dst) {

        this.mp4Src = mp4Src;
        this.mp4Dst = mp4Dst;

        String[] splittedFileName = mp4Src.split("/");
        this.fileName = splittedFileName[splittedFileName.length-1].split(Pattern.quote("."))[0];
        this.fileExtension = "." + splittedFileName[splittedFileName.length-1].split(Pattern.quote("."))[1];

    }

    public void transformFile() {

        rescaleVideo(1280,720);
        rescaleVideo(640,480);
        rescaleVideo(320,200);
        segmentFile("720p");
        segmentFile("480p");
        segmentFile("200p");
        createMPDFile();

    }

    public void segmentFile(String resolution) {

        try {

            inputStream = new FileInputStream(mp4Dst + fileName + resolution + fileExtension);

            byte[] bytesToWrite = new byte[1024000];
            int i = 0;
            while(inputStream.read(bytesToWrite, 0, 1024000) != -1) {

                File copiedVideo = new File((mp4Dst + "video/" + resolution + "/" + fileName + resolution + i + fileExtension));
                FileOutputStream fileOutputStream = new FileOutputStream(copiedVideo);
                fileOutputStream.write(bytesToWrite);
                fileOutputStream.close();
                i++;

            }

            resolutions.add(new Representation(resolution, i));

        }catch (Exception e) {

            System.out.println(e.getClass());
        }

    }


    private void rescaleVideo(Integer widith, Integer height) {

        MyVideoListener myVideoListener = new MyVideoListener(widith,height);
        Resizer resizer = new Resizer(widith,height);

        IMediaReader reader = ToolFactory.makeReader(mp4Src);
        reader.addListener(resizer);

        IMediaWriter writer = ToolFactory.makeWriter(mp4Dst + fileName + height + "p" + fileExtension);
        resizer.addListener(writer);
        writer.addListener(myVideoListener);

        IContainerFormat containerFormat = IContainerFormat.make();
        containerFormat.setOutputFormat("MPEG-4", null, "video/mp4");
        writer.getContainer().setFormat(containerFormat);
        writer.addVideoStream(0, 0, CODEC_ID_H264 , widith, height);
        writer.addAudioStream(1,0, 2, 44100);
        writer.setMaskLateStreamExceptions(true);

        while (reader.readPacket() == null) {
            // continue coding
        }

    }

    public void createMPDFile() {

        Document dom;

        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        try {

            DocumentBuilder db = dbf.newDocumentBuilder();
            dom = db.newDocument();

            Element rootElement = dom.createElement("MPD");
            dom.appendChild(rootElement);

            Element period = dom.createElement("Period");
            rootElement.appendChild(period);

            Element baseURL = dom.createElement("BaseURL");
            baseURL.appendChild(dom.createTextNode(fileName + "/"));
            period.appendChild(baseURL);

            for(Representation representation: resolutions) {

                Element adaptationSet = dom.createElement("AdaptationSet");
                Attr attr = dom.createAttribute("mimeType");
                attr.setValue("video/mp4");
                adaptationSet.setAttributeNode(attr);
                period.appendChild(adaptationSet);

                Element baseURLTemp = dom.createElement("BaseURL");
                baseURLTemp.appendChild(dom.createTextNode("video/"));
                adaptationSet.appendChild(baseURLTemp);

                Element rep = dom.createElement("Representation");
                attr = dom.createAttribute("id");
                attr.setValue(representation.resolution);
                rep.setAttributeNode(attr);
                adaptationSet.appendChild(rep);

                Element baseURLTemp2 = dom.createElement("BaseURL");
                baseURLTemp2.appendChild(dom.createTextNode(representation.resolution + "/"));
                rep.appendChild(baseURLTemp2);

                Element segmentList = dom.createElement("SegmentList");
                rep.appendChild(segmentList);

                for(int a = 0; a < representation.numberOfSeguiments; a++){
                    Element segmentURL = dom.createElement("SegmentURL");
                    attr = dom.createAttribute("media");
                    attr.setValue(fileName + representation.resolution + fileExtension);
                    segmentURL.setAttributeNode(attr);
                    segmentList.appendChild(segmentURL);
                }
            }

            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();
            DOMSource source = new DOMSource(dom);
            StreamResult result = new StreamResult(new File(mp4Dst + "mpd.xml"));
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            transformer.transform(source,result);

        }catch (Exception exception) {

            System.out.println(exception.getClass());
            System.out.println(exception.getMessage());
            System.out.println(exception.getCause());

        }

    }

}
