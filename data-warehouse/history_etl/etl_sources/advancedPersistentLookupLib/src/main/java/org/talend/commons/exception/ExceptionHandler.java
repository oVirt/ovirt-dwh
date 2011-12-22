// ============================================================================
//
// Copyright (C) 2006-2011 Talend Inc. - www.talend.com
//
// This source code is available under agreement available at
// %InstallDIR%\features\org.talend.rcp.branding.%PRODUCTNAME%\%PRODUCTNAME%license.txt
//
// You should have received a copy of the agreement
// along with this program; if not, write to Talend SA
// 9 rue Pages 92150 Suresnes, France
//
// ============================================================================
package org.talend.commons.exception;


/**
 * Implementation of exception handling strategy.<br/>
 * 
 * $Id: ExceptionHandler.java 7038 2007-11-15 14:05:48Z plegall $
 * 
 */
public final class ExceptionHandler {

    /**
     * Empty constructor.
     */
    private ExceptionHandler() {
    }
  
    public static void log(String message) {
    	System.err.println(message);
    }

    public static void process(Throwable ex) {
        	System.err.println(ex.getMessage());
    }

    public static void processForSchemaImportXml(Throwable ex) {
        System.err.println(ex.getMessage());
    }
}
