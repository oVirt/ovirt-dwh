// ============================================================================
//
// Copyright (C) 2006-2010 Talend Inc. - www.talend.com
//
// This source code is available under agreement available at
// %InstallDIR%\features\org.talend.rcp.branding.%PRODUCTNAME%\%PRODUCTNAME%license.txt
//
// You should have received a copy of the agreement
// along with this program; if not, write to Talend SA
// 9 rue Pages 92150 Suresnes, France
//
// ============================================================================
package org.talend.commons.utils.time;

import java.util.HashMap;

/**
 * Timer to measure elapsed time of any process or between steps.
 * 
 * $Id: TimeMeasure.java 46952 2010-08-18 08:41:09Z nrousseau $
 * 
 */
public class TimeMeasure {

    // PTODO create junit test class
    private static HashMap<String, TimeStack> timers;

    private static int indent = 0;

    /**
     * measureActive is true by default. A true value means that all methods calls are processed else no one.
     */
    public static boolean measureActive = true;

    /**
     * display is true by default. A true value means that all informations are displayed.
     */
    public static boolean display = true;

    public static boolean displaySteps = true;

    /**
     * 
     * DOC amaumont Comment method "start".
     * 
     * @param idTimer
     */
    public static void begin(String idTimer) {
        if (!measureActive) {
            return;
        }
        init();
        if (timers.containsKey(idTimer)) {
            if (display) {
                System.out.println(indent(indent) + "Warning (start): timer " + idTimer + " already exists"); //$NON-NLS-1$  //$NON-NLS-2$
            }
        } else {
            indent++;
            TimeStack times = new TimeStack();
            timers.put(idTimer, times);
            if (display) {
                System.out.println(indent(indent) + "Start '" + idTimer + "' ..."); //$NON-NLS-1$  //$NON-NLS-2$
            }
        }
    }

    /**
     * 
     * DOC amaumont Comment method "end".
     * 
     * @param idTimer
     * @return total elapsed time since start in ms
     */
    public static long end(String idTimer) {
        if (!measureActive) {
            return 0;
        }
        init();
        if (!timers.containsKey(idTimer)) {
            if (display) {
                System.out.println(indent(indent) + "Warning (end): timer " + idTimer + " doesn't exist"); //$NON-NLS-1$  //$NON-NLS-2$
            }
            return -1;
        } else {
            TimeStack timeStack = timers.get(idTimer);
            timers.remove(idTimer);
            long elapsedTimeSinceLastRequest = timeStack.getLastStepElapsedTime();
            if (display && displaySteps) {
                System.out.println(indent(indent) + "End '" + idTimer + "', elapsed time since last request: " //$NON-NLS-1$  //$NON-NLS-2$
                        + elapsedTimeSinceLastRequest + " ms "); //$NON-NLS-1$
            }
            long totalElapsedTime = timeStack.getTotalElapsedTime();
            if (display) {
                System.out.println(indent(indent) + "End '" + idTimer + "', total elapsed time: " + totalElapsedTime + " ms "); //$NON-NLS-1$  //$NON-NLS-2$  //$NON-NLS-3$
            }
            indent--;
            return totalElapsedTime;
        }
    }

    /**
     * 
     * DOC amaumont Comment method "timeSinceStart".
     * 
     * @param idTimer
     * @return total elapsed time since start in ms
     */
    public static long timeSinceBegin(String idTimer) {
        if (!measureActive) {
            return 0;
        }
        init();
        if (!timers.containsKey(idTimer)) {
            if (display) {
                System.out.println(indent(indent) + "Warning (end): timer " + idTimer + " does'nt exist"); //$NON-NLS-1$  //$NON-NLS-2$
            }
            return -1;
        } else {
            long time = timers.get(idTimer).getTotalElapsedTime();
            if (display) {
                System.out.println(indent(indent) + "-> '" + idTimer + "', elapsed time since start: " + time + " ms "); //$NON-NLS-1$  //$NON-NLS-2$  //$NON-NLS-3$
            }
            return time;
        }
    }

    /**
     * 
     * DOC amaumont Comment method "timeStep".
     * 
     * @param idTimer
     * @return elapsed time since previous step in ms
     */
    public static long step(String idTimer, String stepName) {
        if (!measureActive) {
            return 0;
        }
        init();
        if (!timers.containsKey(idTimer)) {
            if (display) {
                System.out.println(indent(indent) + "Warning (end): timer " + idTimer + " does'nt exist"); //$NON-NLS-1$  //$NON-NLS-2$
            }
            return -1;
        } else {
            TimeStack timeStack = timers.get(idTimer);
            timeStack.addStep();
            long time = timeStack.getLastStepElapsedTime();
            if (display && displaySteps) {
                System.out.println(indent(indent) + "-> '" + idTimer + "', step name '" + stepName //$NON-NLS-1$  //$NON-NLS-2$
                        + "', elapsed time since previous step: " + time + " ms "); //$NON-NLS-1$  //$NON-NLS-2$
            }
            return time;
        }
    }

    public static void pause(String idTimer) {
        if (!measureActive) {
            return;
        }
        init();
        if (!timers.containsKey(idTimer)) {
            if (display) {
                System.out.println(indent(indent) + "Warning (end): timer " + idTimer + " does'nt exist"); //$NON-NLS-1$  //$NON-NLS-2$
            }
            return;
        } else {
            TimeStack time = timers.get(idTimer);
            // long time = times.getElapsedTimeSinceLastRequest();
            time.pause();
            if (display) {
            }
        }
    }

    public static void resume(String idTimer) {
        if (!measureActive) {
            return;
        }
        init();
        if (!timers.containsKey(idTimer)) {
            begin(idTimer);
            // if (display) {
            //                System.out.println(indent(indent) + "Warning (end): timer " + idTimer + " does'nt exist"); //$NON-NLS-1$  //$NON-NLS-2$
            // }
            return;
        } else {
            TimeStack times = timers.get(idTimer);
            long time = times.getLastStepElapsedTime();
            times.resume();
            if (display) {
            }
        }
    }

    /**
     * DOC amaumont Comment method "init".
     */
    private static void init() {
        if (timers == null) {
            timers = new HashMap<String, TimeStack>();
        }
    }

    public static String indent(final int i) {
        StringBuilder stringBuilder = new StringBuilder();
        for (int j = 0; j < i; j++) {
            stringBuilder.append("  "); //$NON-NLS-1$
        }
        return stringBuilder.toString();
    }

    public static void main(String[] args) {
        try {
            TimeMeasure.begin("a"); //$NON-NLS-1$
            // TimeMeasure.end("b");
            Thread.sleep(500);
            TimeMeasure.step("a", "1"); //$NON-NLS-1$ //$NON-NLS-2$
            Thread.sleep(800);
            TimeMeasure.pause("a"); //$NON-NLS-1$
            Thread.sleep(600);
            TimeMeasure.step("a", "2"); //$NON-NLS-1$ //$NON-NLS-2$
            TimeMeasure.resume("a"); //$NON-NLS-1$
            Thread.sleep(2000);
            TimeMeasure.end("a"); //$NON-NLS-1$
        } catch (InterruptedException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
}
