import DashConverter.DashConverter;

public class Main {

    public static void main(String[] args) throws Exception {
//        Client client = new Client();
//
//        // Parsing the arguments: 0 - server host ; 1 - server port
//        client.fileName = "tame_impala.mp4";
//        int serverPort = 5004;
//        String serverHost = "10.0.2.15";
//
//        InetAddress ServerIPAddr = InetAddress.getByName(serverHost);
//
//        // Establish a connection  (TCP) with the server
//        client.socket = new Socket(ServerIPAddr, serverPort);
//
//        // Initialize input and output buffers
//        client.reader = new BufferedReader(new InputStreamReader(client.socket.getInputStream()));
//        client.writer = new BufferedWriter(new OutputStreamWriter(client.socket.getOutputStream()));

//        client.sendRequest(State.INIT);
//        client.parseResponse();
//        client.sendRequest(State.PLAY);
//        client.parseResponse();


        DashConverter dashConverter = new DashConverter("tame_impala.mp4", "/home/michellamin/Downloads/crazyshit/");
        dashConverter.transformFile();
    }
}
