package org.ovirt.engine.dwh.etltermination;

public class Termination {

    private static volatile Termination instance;

    private boolean terminate;

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
        }));
    }

    public boolean shouldTerminate() {
        return terminate;
    }

}
