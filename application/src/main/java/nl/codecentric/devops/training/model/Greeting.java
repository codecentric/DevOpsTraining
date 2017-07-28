package nl.codecentric.devops.training.model;

/**
 * Created by hylke on 16/07/2017.
 */
public class Greeting {

    private final String hostName;

    private final String environment;

    private final String version;

    private final Long counter;

    public Greeting(String hostName, String environment, final String version, Long counter) {
        this.hostName = hostName;
        this.environment = environment;
        this.version = version;
        this.counter = counter;
    }


    public String getHostName() {
        return hostName;
    }

    public String getEnvironment() {
        return environment;
    }

    public Long getCounter() {
        return counter;
    }

    public String getVersion() {
        return version;
    }
}
