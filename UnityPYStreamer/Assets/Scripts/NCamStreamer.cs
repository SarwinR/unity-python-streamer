using System.Collections.Generic;
using System.Net.Sockets;
using System.Threading;
using UnityEngine;

public class NCameraStreamer : MonoBehaviour
{
    Thread thread;

    public int width, height;

    public string host = "127.0.0.1";
    public int port = 1234;

    private RenderTexture renderTexture;
    private Socket socket;
    private bool connected;

    private Queue<byte[]> buffer;

    public NCameraStreamer(string host, int port)
    {
        this.host = host;
        this.port = port;
        buffer = new Queue<byte[]>();
    }

    void Start()
    {
        // Initialize the texture
        renderTexture = new RenderTexture(720, 480, 24, RenderTextureFormat.ARGB32);
        Camera.main.targetTexture = renderTexture;

        // Start the connection process in a separate thread
        connected = false;

        thread = new Thread(SendFrame);
        thread.Start();
    }

    void SendFrame(object data)
    {
        print(data);
        while (true)
        {
            if (connected)
            {
                if (buffer.TryPeek(out byte[] bufferData))
                {
                    try
                    {
                        socket.Send(bufferData);
                    }
                    catch
                    {
                        connected = false;
                        print("Lost connection!");
                    }
                }
            }
            else
            {
                try
                {
                    // Attempt to connect to the server
                    socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
                    socket.Connect(host, port);

                    // Connection successful
                    connected = true;
                    Debug.Log("Connected to " + host + ":" + port);
                }
                catch (SocketException e)
                {
                    // Connection failed
                    Debug.LogWarning("Failed to connect to " + host + ":" + port + " - " + e.Message);
                }
            }
        }
    }

    void TryConnect()
    {
        if (!connected)
        {
            try
            {
                // Attempt to connect to the server
                socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
                socket.Connect(host, port);

                // Connection successful
                connected = true;
                Debug.Log("Connected to " + host + ":" + port);
            }
            catch (SocketException e)
            {
                // Connection failed
                Debug.LogWarning("Failed to connect to " + host + ":" + port + " - " + e.Message);

            }
        }
    }

    void OnApplicationQuit()
    {
        if (connected)
        {
            socket.Close();
        }

        thread.Abort();
    }
}