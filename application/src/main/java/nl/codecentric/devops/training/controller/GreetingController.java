package nl.codecentric.devops.training.controller;

import nl.codecentric.devops.training.model.Greeting;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.concurrent.atomic.AtomicLong;

/**
 * Created by hylke on 16/07/2017.
 */
@RestController
public class GreetingController {

    private static String serverAddress;

    private final AtomicLong counter = new AtomicLong();

    @Value("${environment:unknown}")
    private String environment;

    @Value("${version:unknown}")
    private String version;


    static {
        try {
            serverAddress = InetAddress.getLocalHost().getHostName();
        } catch (UnknownHostException e) {
            // DO nothing
        }
    }

    @RequestMapping("/")
    public Greeting greeting() {
        return new Greeting(serverAddress, this.environment, this.version,counter.getAndIncrement());
    }
}
