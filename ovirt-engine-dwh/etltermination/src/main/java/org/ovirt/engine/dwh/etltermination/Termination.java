package org.ovirt.engine.dwh.etltermination;

public class Termination {

    private static volatile Termination instance;

    private boolean terminate;
    private boolean stop;

    public static Termination getInstance() {
        if (instance == null) {
            synchronized(Termination.class) {
                if (instance == null) {
                    instance = new Termination();
                }
            }
        }
        return instance;
    }

    private Termination() {
        terminate = false;

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            terminate = true;
            try {
                while (!stop) {
                    Thread.sleep(100);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }));
    }

    public boolean shouldTerminate() {
        return terminate;
    }

    public void stop() {
        stop = true;
    }
}
