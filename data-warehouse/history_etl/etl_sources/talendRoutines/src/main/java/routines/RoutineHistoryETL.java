package routines;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.text.ParseException;

/*
 * user specification: the function's comment should contain keys as follows: 1. write about the function's comment.but
 * it must be before the "{talendTypes}" key.
 * 
 * 2. {talendTypes} 's value must be talend Type, it is required . its value should be one of: String, char | Character,
 * long | Long, int | Integer, boolean | Boolean, byte | Byte, Date, double | Double, float | Float, Object, short |
 * Short
 * 
 * 3. {Category} define a category for the Function. it is required. its value is user-defined .
 * 
 * 4. {param} 's format is: {param} <type>[(<default value or closed list values>)] <name>[ : <comment>]
 * 
 * <type> 's value should be one of: string, int, list, double, object, boolean, long, char, date. <name>'s value is the
 * Function's parameter name. the {param} is optional. so if you the Function without the parameters. the {param} don't
 * added. you can have many parameters for the Function.
 * 
 * 5. {example} gives a example for the Function. it is optional.
 */
public class RoutineHistoryETL {

    /**
     * Reset date to start of day.
     * 
     * @param The date to reset.
     * 
     * {talendTypes} Date
     * 
     * {Category} User Defined
     * 
     * {param} date(givenDate) date : The date given.
     * 
     * {example} startOfHour(01/01/2000 01:10:25) return 01/01/2000 00:00:00 #
     */
	
    public static Date startOfDay(Date date) {
        if (date == null) {
            return null;
        }
    	Calendar cal = Calendar.getInstance();       // get calendar instance
    	cal.setTime(date);                           // set cal to date
    	cal.set(Calendar.HOUR_OF_DAY, 0);            // set hour to midnight
    	cal.set(Calendar.MINUTE, 0);                 // set minute in hour
    	cal.set(Calendar.SECOND, 0);                 // set second in minute
    	cal.set(Calendar.MILLISECOND, 0);            // set millis in second
    	return cal.getTime();             // actually computes the new Date
    }

    /**
     * Reset date to start of hour.
     * 
     * @param The date to reset.
     * 
     * {talendTypes} Date
     * 
     * {Category} User Defined
     * 
     * {param} date(givenDate) date : The date given.
     * 
     * {example} startOfHour(01/01/2000 01:10:25) return 01/01/2000 01:00:00 #
     */
    
    public static Date startOfHour(Date date) {
    	if (date == null) {
            return date;
        }
    	Calendar cal = Calendar.getInstance();       // get calendar instance
    	cal.setTime(date);                           // set cal to date
    	cal.set(Calendar.MINUTE, 0);                 // set minute in hour
    	cal.set(Calendar.SECOND, 0);                 // set second in minute
    	cal.set(Calendar.MILLISECOND, 0);            // set millis in second
    	return cal.getTime();            			 // actually computes the new Date	
    } 
    
    /**
     * Reset date to start of minute.
     * 
     * @param The date to reset.
     * 
     * {talendTypes} Date
     * 
     * {Category} User Defined
     * 
     * {param} date(givenDate) date : The date given.
     * 
     * {example} startOfMinute(01/01/2000 01:10:25) return 01/01/2000 01:10:00 #
     */
    
    public static Date startOfMinute(Date date) {
    	if (date == null) {
            return date;
        }
    	Calendar cal = Calendar.getInstance();       // get calendar instance
    	cal.setTime(date);                           // set cal to date
    	cal.set(Calendar.SECOND, 0);                 // set second in minute
    	cal.set(Calendar.MILLISECOND, 0);            // set millis in second
    	return cal.getTime();            			 // actually computes the new Date	
    } 
    
    /**
     * Reset date to start of second.
     * 
     * @param The date to reset.
     * 
     * {talendTypes} Date
     * 
     * {Category} User Defined
     * 
     * {param} date(givenDate) date : The date given.
     * 
     * {example} startOfMinute(01/01/2000 01:10:25.0155421) return 01/01/2000 01:10:25 #
     */
    
    public static Date startOfSecond(Date date) {
    	if (date == null) {
            return date;
        }
    	Calendar cal = Calendar.getInstance();       // get calendar instance
    	cal.setTime(date);                           // set cal to date
    	cal.set(Calendar.MILLISECOND, 0);            // set millis in second
    	return cal.getTime();            			 // actually computes the new Date	
    } 
    
    /**
     * Compares two dates
     * @param date1 (first date)
     * @param date2 (second date)
     * @return the result whether two date is the same, if first one less than second one return number -1, equals
     * return number 0, bigger than return number 1.
     * 
     * {talendTypes} Integer
     * 
     * {Category} User Defined
     * 
     * {param} date(Date1) date1 : the first date to compare
     * 
     * {param} date(Date2) date2 : the second date to compare
     * 
     *  {examples}
     * 
     * ->> compareDate(01/01/2000 01:10:25, 01/01/2010 16:10:35) return -1
     * 
     * ->> compareDate(01/01/2010 16:10:35, 01/01/2000 01:10:25) return 1
     * 
     * ->> compareDate(01/01/2010 16:10:35, 01/01/2010 16:10:35) return 0 #
     */
    
    public static int dateCompare(Date date1, Date date2){
        if (date1 == null && date2 == null) {
            return 0;
        } else if (date1 != null && date2 == null) {
            return 1;
        } else if (date1 == null && date2 != null) {
            return -1;
        }
        Calendar cal1 = Calendar.getInstance();
        Calendar cal2 = Calendar.getInstance();
        cal1.setTime(date1);
        cal2.setTime(date2);
        if(cal1.before(cal2)){
        	return -1;}
        else if(cal1.after(cal2)){
        	return 1;}
        else{
        	return 0;}
    }
    
    /**
     * Manipulate date
     * 
     * @param date
     * @param changeamount (the number to add subtract from date part)
     * @param date part to change
     * @return the manipulated date.
     * 
     * {talendTypes} Date
     * 
     * {Category} User Defined
     * 
     * {param} date(Date) date : the date to manipulate.
     * 
     * {param} integer(changeAmount) changeAmount : the number to add subtract from date part
     * 
     * {param} String(datePart) datePart : which part to add or subtract from.
     * 
     *  {example} manipulateDate(01/01/2010 16:10:35, 5, HH) return 01/01/2010 21:10:35 #
     */
    
    public static Date manipulateDate(Date date, int changeAmount, String datePart) {
        if (date == null) {
            return date;
        }
        Calendar cal = Calendar.getInstance();
        cal.setTime(date);
        if (datePart.equals("SSS")){ //$NON-NLS-1$
        	cal.add(Calendar.MILLISECOND, changeAmount);
        	return cal.getTime();
        }  
        else if (datePart.equals("ss")){ //$NON-NLS-1$
        	cal.add(Calendar.SECOND, changeAmount);
        	return cal.getTime();
        }  
        else if (datePart.equals("mm")){ //$NON-NLS-1$
        	cal.add(Calendar.MINUTE, changeAmount);
        	return cal.getTime();
        }   
        else if (datePart.equals("HH")){ //$NON-NLS-1$
        	cal.add(Calendar.HOUR_OF_DAY, changeAmount);
        	return cal.getTime();
        }   
        else if (datePart.equals("dd")){ //$NON-NLS-1$
        	cal.add(Calendar.DATE, changeAmount);
        	return cal.getTime();
        }
        else if (datePart.equals("MM")){ //$NON-NLS-1$
        	cal.add(Calendar.MONTH, changeAmount);
        	return cal.getTime();
        }
        else if (datePart.equals("yyyy")){ //$NON-NLS-1$
        	cal.add(Calendar.YEAR, changeAmount);
        	return cal.getTime();
        }
        else{
        	throw new IllegalArgumentException("Does not support the date part: " + datePart);
        }
      }
    
    /**
     * Formats Date to Date\Time String.
     * 
     * @param date
     * @param pattern (the date\time string pattern)
     * @return the new date\time String.
     * @throws ParseException 
     * 
     * {talendTypes} String
     * 
     * {Category} User Defined
     * 
     * {param} date(Date) date : the date to output.
     * 
     * {param} String(pattern) pattern : the pattern to output.
     * 
     * 
     * {example} dateFormat(01/01/2010 16:10:35, "MM-dd-yyyy") return 01-01-2010 string #
     * 
     */
    
    public static String dateFormat(Date date, String pattern) throws ParseException {
        // Make a SimpleDateFormat for toString()'s output.        
        SimpleDateFormat format = new SimpleDateFormat(pattern);
        return format.format(date);
    }

    /**
     * Returns the difference between two dates.
     * 
     * @param date1
     * @param date2
     * @param datePart (the date\time string part)
     * @return the difference between the two dates.
     * @throws ParseException 
     * 
     * {talendTypes} Date
     * 
     * {Category} User Defined
     * 
     * {param} date1(Date) date : the first date.
     * 
     * {param} date1(Date) date : the second date.
     * 
     * {param} String(datePart) date part : the unit to return.
     * 
     * 
     * {example} dateDifference(01/01/2010 16:10:35, 01/01/2010 16:10:00, "ss") return 35 #
     * 
     */
    
    public static long dateDifference(Date date1, Date date2, String datePart)
    {
        // Creates two calendars instances
        Calendar cal1 = Calendar.getInstance();
        Calendar cal2 = Calendar.getInstance();

        // Set the date for both of the calendar instance
        cal1.setTime(date1);
        cal2.setTime(date2);
        
        // Get the represented date in milliseconds
        long milis1 = cal1.getTimeInMillis();
        long milis2 = cal2.getTimeInMillis();

        // Calculate difference in milliseconds
        long diff = milis1 - milis2;
        
        if (datePart.equals("SSS")){ //$NON-NLS-1$
        	return diff;
        }  
        else if (datePart.equals("ss")){ //$NON-NLS-1$
            // Calculate difference in seconds
        	return diff / 1000;
        }  
        else if (datePart.equals("mm")){ //$NON-NLS-1$
            // Calculate difference in minutes
        	return diff / (60 * 1000);
        }   
        else if (datePart.equals("HH")){ //$NON-NLS-1$
            // Calculate difference in hours
        	return diff / (60 * 60 * 1000);
        }   
        else if (datePart.equals("dd")){ //$NON-NLS-1$
            // Calculate difference in days
        	return diff / (24 * 60 * 60 * 1000);
        }
        else{
        	throw new IllegalArgumentException("Does not support the date part: " + datePart);
        }
    }
}
