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
import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;

import org.talend.designer.components.lookup.common.ILookupManagerUnit;
import org.talend.designer.components.persistent.IRowProvider;

import routines.system.IPersistableLookupRow;

/**
 * 
 * Abstract class for ordered beans used in lookups with "Store on disk".
 * 
 * @see http://www.talendforge.org/bugs/view.php?id=6780#bugnotes
 * 
 * @param <B> bean
 */
public abstract class AbstractOrderedBeanLookup<B extends Comparable<B> & IPersistableLookupRow<B>> implements
        ILookupManagerUnit<B> {

    protected static final int MARK_READ_LIMIT = 256 * 1024 * 1024;

    protected static final int KEYS_SIZE_PLUS_VALUES_SIZE = 8;

    protected BufferedInputStream keysBufferedInStream;

    protected ObjectInputStream keysObjectInStream;

    protected DataInputStream valuesDataInStream;

    protected ObjectInputStream valuesObjectInStream;

    protected long length;

    protected B lookupInstance;

    protected int currentValuesSize;

    protected long skipValuesSize;

    protected long countBeansToSkip;

    protected boolean nextDirty = true;

    protected boolean noMoreNext;

    protected B previousAskedKey;

    protected long markCursorPosition = -1;

    protected B currentSearchedKey;

    protected boolean hasNext;

    protected boolean atLeastOneLoadkeys = false;

    protected boolean startWithNewKey;

    protected IRowProvider<B> rowProvider;

    protected boolean nextWithPreviousLookup;

    protected int remainingSkip;

    protected boolean previousCompareResultMatch;

    protected B previousLookupInstance;

    protected int sizeDataToRead;

    protected B resultLookupInstance;

    protected int fileIndex;

    private boolean skipBytesEnabled;

    /**
     * 
     * DOC amaumont OrderedBeanLookup constructor comment.
     * 
     * @param keysFilePath
     * @param valuesFilePath
     * @param fileIndex
     * @param skipBytesEnabled
     * @param internalKeyInstance
     * @param keys_management
     * @throws IOException
     */
    public AbstractOrderedBeanLookup(String keysFilePath, String valuesFilePath, int fileIndex, IRowProvider<B> rowProvider,
            boolean skipBytesEnabled) throws IOException {
        File keysDataFile = new File(keysFilePath);
        this.length = keysDataFile.length();

        this.fileIndex = fileIndex;

        this.keysBufferedInStream = new BufferedInputStream(new FileInputStream(keysDataFile));
        this.keysObjectInStream = new ObjectInputStream(keysBufferedInStream);
        this.valuesDataInStream = new DataInputStream(new BufferedInputStream(new FileInputStream(valuesFilePath)));
        this.valuesObjectInStream = new ObjectInputStream(valuesDataInStream);
        this.lookupInstance = rowProvider.createInstance();
        this.previousAskedKey = rowProvider.createInstance();
        this.rowProvider = rowProvider;

        this.skipBytesEnabled = skipBytesEnabled;

        // readDescriptors();

    }

    private void readDescriptors() throws IOException {
        int countObjects = valuesDataInStream.readInt();
        for (int i = 0; i < countObjects; i++) {
            try {
                Object readObject = valuesObjectInStream.readObject();
                System.out.println(readObject);
            } catch (ClassNotFoundException e) {
                throw new RuntimeException(e);
            }
        }
    }

    /*
     * (non-Javadoc)
     * 
     * @see org.talend.designer.components.persistent.ILookupManager#lookup(B)
     */
    public abstract void lookup(B key) throws IOException;

    /*
     * (non-Javadoc)
     * 
     * @see org.talend.designer.components.persistent.ILookupManager#hasNext()
     */
    public abstract boolean hasNext() throws IOException;

    /*
     * (non-Javadoc)
     * 
     * @see org.talend.designer.components.persistent.ILookupManager#next()
     */
    public abstract B next() throws IOException;

    protected void loadDataKeys(B lookupInstance) throws IOException {
        atLeastOneLoadkeys = true;
        lookupInstance.readKeysData(keysObjectInStream);
        currentValuesSize = keysObjectInStream.readInt();
    }

    protected boolean isEndOfKeysFile() throws IOException {
        return !(keysObjectInStream.available() > 0 || keysBufferedInStream
                .available() > 0);
    }

    protected void loadDataValues(B lookupInstance, int valuesSize) throws IOException {
        if (skipValuesSize > 0) {
            skipValuesSize += remainingSkip;

            if (skipBytesEnabled) {
                int currentSkipped = 0;
                while (skipValuesSize != (currentSkipped += valuesDataInStream.skip(skipValuesSize - currentSkipped)))
                    ;
            } else {
                for (long i = 0; i < countBeansToSkip; i++) {
                    lookupInstance.readValuesData(valuesDataInStream, valuesObjectInStream);
                }
            }

            // System.out.println("Data skipped:" + skipValuesSize);
            remainingSkip = 0;
            skipValuesSize = 0;
            countBeansToSkip = 0;
        }
        lookupInstance.readValuesData(valuesDataInStream, valuesObjectInStream);

    }

    /*
     * (non-Javadoc)
     * 
     * @see org.talend.designer.components.persistent.ILookupManager#close()
     */
    public void close() throws IOException {

        if (keysObjectInStream != null) {
            keysObjectInStream.close();
        }
        if (keysBufferedInStream != null) {
            keysBufferedInStream.close();
        }
        if (valuesDataInStream != null) {
            valuesObjectInStream.close();
        }
        if (valuesDataInStream != null) {
            valuesDataInStream.close();
        }
    }

}
