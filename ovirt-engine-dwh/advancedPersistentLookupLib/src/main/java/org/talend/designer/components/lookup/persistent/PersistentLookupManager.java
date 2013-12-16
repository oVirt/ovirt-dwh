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
package org.talend.designer.components.lookup.persistent;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

import org.talend.designer.components.lookup.common.ICommonLookup.MATCHING_MODE;
import org.talend.designer.components.persistent.IRowCreator;
import org.talend.designer.components.persistent.utils.FileUtils;

import routines.system.IPersistableRow;

/**
 * Manager for lookup type 'ALL_ROWS'.
 * 
 * @see http://www.talendforge.org/bugs/view.php?id=6780#bugnotes
 * 
 * @param <B> bean
 */
public class PersistentLookupManager<B extends IPersistableRow<B>> implements IPersistentLookupManager<B>, Cloneable {

    private String container;

    private ObjectOutputStream objectOutStream;

    private BufferedInputStream bufferedInStream;

    private ObjectInputStream objectInStream;

    private IRowCreator<B> rowCreator;

    private B dataInstance;

    /**
     * PersistentLookupManager constructor.
     * 
     * @param container
     * @throws IOException
     */
    public PersistentLookupManager(MATCHING_MODE matchingMode, String container, IRowCreator<B> rowCreator) throws IOException {
        super();
        this.container = container;
        this.rowCreator = rowCreator;
        FileUtils.createParentFolderIfNotExists(container);
    }

    public void initPut() throws IOException {

        objectOutStream = new ObjectOutputStream(new BufferedOutputStream(new FileOutputStream(buildDataFilePath())));
        this.dataInstance = this.rowCreator.createRowInstance();

    }

    private String buildDataFilePath() {
        return container + "_Data.bin"; //$NON-NLS-1$
    }

    public void put(B bean) throws IOException {
        bean.writeData(objectOutStream);
    }

    public void endPut() throws IOException {

        objectOutStream.close();

    }

    public void initGet() throws IOException {

        initDataIn();
        this.dataInstance = this.rowCreator.createRowInstance();

    }

    public void lookup(B key) throws IOException {

        if (this.objectInStream != null) {
            this.objectInStream.close();
        }
        if (this.bufferedInStream != null) {
            this.bufferedInStream.close();
        }

        initDataIn();

    }

    private void initDataIn() throws IOException {
        this.bufferedInStream = new BufferedInputStream(new FileInputStream(buildDataFilePath()));
        this.objectInStream = new ObjectInputStream(bufferedInStream);
    }

    public B getNextFreeRow() {
        return this.dataInstance;
    }

    public boolean hasNext() throws IOException {
        return this.objectInStream.available() > 0 || this.bufferedInStream.available() > 0;
    }

    public B next() throws IOException {
        dataInstance.readData(this.objectInStream);
        return dataInstance;
    }

    public void endGet() throws IOException {

        if (this.objectInStream != null) {
            this.objectInStream.close();
        }
        if (this.bufferedInStream != null) {
            this.bufferedInStream.close();
        }

        File file = new File(buildDataFilePath());
        file.delete();

    }

    public void clear() throws IOException {

    }

    @Override
    public Object clone() throws CloneNotSupportedException {
        return super.clone();
    }

}
