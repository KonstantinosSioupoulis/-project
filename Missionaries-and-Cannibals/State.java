import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;
public class State implements Comparable<State>
{
	//heuristic score variables
	private int score;
	private int costFromRoot;
	private State father = null;
	private int cannibalsLeft;
	private int missionariesLeft;
	private int cannibalsRight;
	private int missionariesRight;
	private int boatCapacity;
	private int maximumCrossings;
	private boolean boatIsLeft;
	

	public State(int N, int M,int K)
    {
		cannibalsLeft=N;
		missionariesLeft=N;
		
		cannibalsRight=0;
		missionariesRight=0;
		boatCapacity=M;
		maximumCrossings=K;
		boatIsLeft=true;
		score=0;
		costFromRoot=0;
		
    }
	public State(State s){
		this.cannibalsLeft=s.cannibalsLeft;
		this.missionariesLeft=s.missionariesLeft;
		this.cannibalsRight=s.cannibalsRight;
		this.missionariesRight=s.missionariesRight;
		this.score=s.score;
		this.boatIsLeft=s.boatIsLeft;
		this.costFromRoot=s.costFromRoot;
		this.maximumCrossings=s.maximumCrossings;
		this.boatCapacity=s.boatCapacity;
		
	}
	
	
	private boolean moveRight(int missionaries,int cannibals){
		if(missionaries>missionariesLeft || cannibals>cannibalsLeft || missionaries+cannibals==0){
			return false;
		}
		if(missionaries<cannibals && missionaries>0){
			return false;
		}
		missionariesLeft -= missionaries;
		cannibalsLeft -= cannibals;
		
		missionariesRight+=missionaries;
		cannibalsRight+=cannibals;
		
		if((missionariesLeft<cannibalsLeft && missionariesLeft>0) || (missionariesRight<cannibalsRight && missionariesRight>0)){
			return false;
		}
		
		boatIsLeft=false;
		return true;
	}
	
	private boolean moveLeft(int missionaries,int cannibals){
		if(missionaries>missionariesRight|| cannibals>cannibalsRight || missionaries+cannibals==0){
			return false;
		}
		if(missionaries<cannibals && missionaries>0){
			return false;
		}
		missionariesRight -= missionaries;
		cannibalsRight -= cannibals;
		
		missionariesLeft+=missionaries;
		cannibalsLeft+=cannibals;
		
		if((missionariesLeft<cannibalsLeft && missionariesLeft>0) || (missionariesRight<cannibalsRight && missionariesRight>0)){
			return false;
		}
		boatIsLeft=true;
		return true;
	}
	State child;
	int count=0;
	ArrayList<State> getChildren()
	{
		ArrayList<State> children = new ArrayList<State>();
		//State child=new State(this);
		
		count++;
		for(int i=0;i<=boatCapacity;i++)
		{
			for(int j=0;j<=boatCapacity-i;j++)
			{
				child=new State(this);
				if(boatIsLeft)
				{
					//if (j<=i && child.moveRight(i,j))
					if(child.moveRight(i,j))
					{
						child.setFather(this);
						child.evaluate();
					
						if(child.getScore()<=child.maximumCrossings)
						{
							children.add(child);
						}
					}
				}
				else
				{
					if (child.moveLeft(i,j))
					{
						child.setFather(this);
						child.evaluate();
					
						if(child.getScore()<=child.maximumCrossings)
						{
							children.add(child);
						}
					}
				}
				//child.print();
				
			}
		}
		
		return children;
		
	}
	
	
	
	State getFather()
	{
        return this.father;
    }

    void setFather(State father)
	{
        this.father = father;
    }

    int getScore() {return this.score;}
	

    void setScore(int score) {this.score = score;}
	
	
	public int getCostFromRoot(){
		return this.costFromRoot;
	}
	
	private void evaluate()
	{
		this.costFromRoot=(this.getFather()).getCostFromRoot()+1;
		int heuristicScore=this.heuristic();
		this.setScore(costFromRoot+heuristicScore);
		
		
	}
	
	private int heuristic()
	{
		//if(!boatIsLeft && (cannibalsLeft+ missionariesLeft)>0) {return (cannibalsLeft+missionariesLeft)*2;}
		
		//else if (boatIsLeft && (cannibalsLeft + missionariesLeft)<=boatCapacity) {return 1;}
		
	//	else if (boatIsLeft && (cannibalsLeft + missionariesLeft)>1) {return 2*(cannibalsLeft+missionariesLeft)-3;}
		
		if(boatIsLeft)
		{
			if((cannibalsLeft + missionariesLeft)<=boatCapacity) {return 1;}
		
			else
			{
				return (cannibalsLeft+missionariesLeft)/boatCapacity +1;
			}
		}
		else if (!boatIsLeft)
		{
			if((cannibalsLeft + missionariesLeft)<=boatCapacity) {return 2;}
		
			else
			{
				return 2*(cannibalsLeft+missionariesLeft)/boatCapacity + 2;
			}
			
		}
		return 0;
		
	
	}
	
	protected boolean isTerminal()
	{
		if(cannibalsLeft==0 && missionariesLeft==0) {return true;}
		
		else {return false;}
	}
	
	@Override
	public boolean equals(Object obj)	
	{
		if(this.missionariesLeft!=((State)obj).missionariesLeft)
		{
			return false;
		}
		
		if(this.missionariesRight!=((State)obj).missionariesRight)
		{
			return false;
		}
		
		if(this.cannibalsLeft!=((State)obj).cannibalsLeft)
		{
			return false;
		}
		
		if(this.cannibalsRight!=((State)obj).cannibalsRight)
		{
			return false;
		}
		
		if(this.boatIsLeft!=((State)obj).boatIsLeft)
		{
			return false;
		}
		
		return true;
	}
		
	 @Override
    public int hashCode()
    {
        return this.costFromRoot+this.missionariesRight+ this.cannibalsRight;
    }
	
	@Override
    public int compareTo(State s)
    {
        return Double.compare(this.score, s.score); // compare based on the heuristic score.
    }
	

	public void print()
	{
		System.out.println("****************************************************");
		for(int m=0;m<missionariesLeft;m++)
		{
			System.out.print("m");
		}
		System.out.print(" ");
		for(int c=0;c<cannibalsLeft;c++)
		{
			System.out.print("c");
		}
		if(boatIsLeft)
		{
			System.out.print("/==/\t");
		}
		else
		{
			System.out.print("    /==/");
		}
		
		for(int m=0;m<missionariesRight;m++)
		{
			System.out.print("m");
		}
		System.out.print(" ");
		for(int c=0;c<cannibalsRight;c++)
		{
			System.out.print("c");
		}
		
		if (!this.isTerminal())
		{
			System.out.printf("              %d crosses left to cross the river!!",this.maximumCrossings-this.costFromRoot);
		}
		else
		{
			System.out.printf("\t\tCongratulations you crossed the river in %d crosses with %d crosses left!!",costFromRoot,this.maximumCrossings-this.costFromRoot);
		}
			System.out.println("\n****************************************************");
	
	}
	
	
}