import Client.StreamPlayer;
import DashConverter.DashConverter;

public class Main {

    public static void main(String[] args) throws Exception {


        StreamPlayer streamPlayer = new StreamPlayer("/home/michellamin/Documents/tame_impala.mp4");

        DashConverter dashConverter = new DashConverter("tame_impala.mp4", "/home/michellamin/Downloads/crazyshit/");
        dashConverter.transformFile();
    }
}
