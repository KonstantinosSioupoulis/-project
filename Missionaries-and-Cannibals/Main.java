import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;
public class Main
{

	/**
     *
     * To BFS apaitei ekthetiko xwro epomenws poly pithanon h java na xemeinei
     * apo mnhmh prin oloklhrwthei o algorithmos. Trexte thn java me thn
     * parametro -Xmx gia na xeperasete auto to provlhma.
     *
     * e.g. java -Xmx512m Main
	 */
	public static void main(String[] args)
	{
		Scanner in=new Scanner(System.in);
		
		System.out.print("Give number of missionaries:");
		int N=in.nextInt();
		 
		System.out.print("Give number of boat capacity:");
		int M=in.nextInt();
		 
		System.out.print("Give number of maximum crosses:");
		int K=in.nextInt();
		 
		State initialState=new State(N,M,K);
		initialState.print();
		System.out.println("***************");
		SpaceSearcher spaceSearcher = new SpaceSearcher();
		long start = System.currentTimeMillis();
		State terminalState = spaceSearcher.A_STAR_ClosedSet(initialState);
		long end = System.currentTimeMillis();
		if(terminalState == null)
		{
			System.out.println("Could not find a solution.");
		}
		else
			{
				State temp = terminalState;
				ArrayList<State> path = new ArrayList<State>();
				path.add(terminalState);
				while(temp.getFather()!=null)
				{
					path.add(temp.getFather());
					temp = temp.getFather();
				}
				Collections.reverse(path);
				System.out.println("Finished in "+path.size()+" steps!");
				for(State item : path)
				{
					item.print();
				}
			}
		System.out.println("A* with closed set search time: " + (double)(end - start) / 1000 + " sec.");
		 
	}
}
