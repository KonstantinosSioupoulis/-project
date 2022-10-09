import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;

public class SpaceSearcher
{
	private ArrayList<State> states;
	private HashSet<State> closedSet;
	
	SpaceSearcher()
	{
		this.states = null;
		this.closedSet = null;
	}
	
	public State A_STAR_ClosedSet(State initialState)
	{
		this.states = new ArrayList<State>();
		this.closedSet = new HashSet<State>();
		this.states.add(initialState);
		while(this.states.size() > 0)
		{
			State currentState = this.states.remove(0);
			if(currentState.isTerminal())
			{
			
				return currentState;
			}
			if(!closedSet.contains(currentState))
			{
				this.closedSet.add(currentState);
				this.states.addAll(currentState.getChildren());
				Collections.sort(this.states);
			}
			
		}
		return null;
	}
}