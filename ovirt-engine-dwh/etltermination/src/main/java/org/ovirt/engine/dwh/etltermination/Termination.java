package org.ovirt.engine.dwh.etltermination;

public class Termination {

    private static volatile Termination instance;

    private boolean terminate;
    private boolean stopped;

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

    public static void stop() {
        System.out.println("Termination.stop() called");
        getInstance().stopped = true;
    }

    private Termination() {
        terminate = false;
        stopped = false;
        
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            terminate = true;
            
            System.out.println("Shutdown hook waiting for stop() to be called...");
            while (!stopped) {
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    System.out.println("Shutdown hook interrupted while waiting: " + e.getMessage());
                    break;
                }
            }
            System.out.println("Shutdown hook exiting - cleanup completed");
        }));
    }

    public boolean shouldTerminate() {
        return terminate;
    }

}
