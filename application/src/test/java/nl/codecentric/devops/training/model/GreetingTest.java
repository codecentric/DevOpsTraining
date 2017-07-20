package nl.codecentric.devops.training.model;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class GreetingTest {

    private Greeting uut;

    @Before
    public void before() {
        uut = new Greeting("host", "blue", 1L);
    }

    @Test
    public void getHostName() throws Exception {
        assertEquals("host", uut.getHostName());
    }

    @Test
    public void getEnvironment() throws Exception {
        assertEquals("blue", uut.getEnvironment());
    }

    @Test
    public void getCounter() throws Exception {
        assertTrue(1L == uut.getCounter());
    }

}