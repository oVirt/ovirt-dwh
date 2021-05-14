package org.ovirt.engine.dwh.etltermination;

import sun.misc.Signal;
import sun.misc.SignalHandler;

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
        SignalHandler sh=new SignalHandler() {
            public void handle(Signal signal) {
                terminate = true;
            }
        };
        Signal.handle(new Signal("TERM"), sh );
        Signal.handle(new Signal("INT"), sh );
    }

    public boolean shouldTerminate() {
        return terminate;
    }

}
