package common.exceptions;

public class CTBTOException extends Exception
{
	 /**
	 * 
	 */
	private static final long	serialVersionUID	= 3257847692590986809L;
	
	/**
	 * Default no message
	 *
	 */
	public ShakraException() 
	{
        super();
    }
	
	/**
	 * Gather arg0 and the message of arg1
	 * @param arg0 string of the message
	 * @param arg1 Cause of the exception
	 */
	public CTBTOException(String arg0, Throwable arg1)
	{
		// gather msg + plus message from Throwable
		super(arg0 + ((arg1 == null) ? "" : ". " + arg1.getMessage()),arg1);
	}
	
    /**
    * Use the message of the passed exception as the message of VMCException
    * @param e a Throwable
    */
    public CTBTOException(Throwable e) 
	{
        super( (e == null ) ? "" : e.getMessage() , e);
    }

    /**
     * Message of the exception
     * @param s message for the exception
     */
    public CTBTOException(String s) {
        super(s);
    }

}