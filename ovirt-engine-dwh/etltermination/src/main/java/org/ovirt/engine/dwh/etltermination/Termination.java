package org.ovirt.engine.dwh.etltermination;

import sun.misc.Signal;
import sun.misc.SignalHandler;

public class Termination {

    private static volatile Termination instance;

    private boolean terminate;

    public static Termination getInstance() {
        if (instance == null) {
            synchronized(Termination.class) {
                instance = new Termination();
            }
        }
        return instance;
    }

    private Termination() {
        terminate = false;
        Signal.handle(new Signal("TERM"), new SignalHandler() {
            public void handle(Signal signal) {
                terminate = true;
            }
        });
    }

    public boolean shouldTerminate() {
        return terminate;
    }

}
