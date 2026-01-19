"""
Healthcare Cost Model and Impact Tool Classes
"""
import pandas as pd


class HealthcareCostModel:
    """Manages healthcare costs and condition mappings"""
    
    def __init__(self, df_healthcare_costs: pd.DataFrame):
        self.df_costs = df_healthcare_costs.set_index('codenaam')
        self.COST_COLUMN = 'kosten per verzekerde 2024'
        self.condition_cost_mapping = self._create_condition_mapping()

    def _create_condition_mapping(self) -> dict:
        return {
            # 1. Mental Health and Stressmanagement
            'Burn-Out': ['Inschrijftarieven', 'Farmaceutische zorg', 'Consulten GGZ', 'Ergotherapie' , 'Gecombineerde leefstijlinterventies (GLI)', 'Fysiotherapie', 'Oefentherapie Mensendieck/Cesar', 'Kosten overige prestaties'],
            'Depression': ['Inschrijftarieven', 'Farmaceutische zorg', 'Consulten GGZ', 'Gecombineerde leefstijlinterventies (GLI)', 'Integrale kosten DBC-zorgproducten gereguleerde segment', 'Integrale kosten DBC-zorgproducten vrije segment', 'Intramuraal verblijf GGZ', 'Kosten overige prestaties'],
            'Anxiety Disorder': ['Inschrijftarieven', 'Farmaceutische zorg', 'Consulten GGZ', 'Gecombineerde leefstijlinterventies (GLI)', 'Intramuraal verblijf GGZ', 'Kosten overige prestaties'],
            'Stress': ['Inschrijftarieven', 'Farmaceutische zorg', 'Consulten GGZ', 'Gecombineerde leefstijlinterventies (GLI)', 'Intramuraal verblijf GGZ', 'Kosten overige prestaties'],

            # 2. Physical Wellbeing and Health
            'Hernia': ['Inschrijftarieven', 'Farmaceutische zorg', 'Fysiotherapie', 'Oefentherapie Mensendieck/Cesar', 'Integrale kosten DBC-zorgproducten gereguleerde segment', 'Integrale kosten DBC-zorgproducten vrije segment'],
            'RSI': ['Inschrijftarieven', 'Farmaceutische zorg', 'Fysiotherapie', 'Ergotherapie', 'Oefentherapie Mensendieck/Cesar'],
            'Osteoarthritis': ['Inschrijftarieven', 'Farmaceutische zorg', 'Fysiotherapie', 'Oefentherapie Mensendieck/Cesar', 'Integrale kosten DBC-zorgproducten gereguleerde segment', 'Integrale kosten DBC-zorgproducten vrije segment'],
            'Cardiovascular diseases': ['Inschrijftarieven', 'Gecombineerde leefstijlinterventies (GLI)', 'Dieetadvisering', 'Farmaceutische zorg', 'Integrale kosten DBC-zorgproducten gereguleerde segment', 'Integrale kosten DBC-zorgproducten vrije segment', 'Add-ons dure geneesmiddelen', 'Fysiotherapie', 'Logopedie', 'Vervoer per ambulance en helikopter'],

            # 3. Diet and Lifestyle Choices
            'Eating disorder': ['Inschrijftarieven', 'Farmaceutische zorg', 'Consulten GGZ', 'Intramuraal verblijf GGZ', 'Dieetadvisering', 'Gecombineerde leefstijlinterventies (GLI)', 'Kosten overige prestaties'],
            'Type 2 diabetes': ['Inschrijftarieven', 'Dieetadvisering', 'Gecombineerde leefstijlinterventies (GLI)', 'Farmaceutische zorg', 'Multidisciplinaire zorg', 'Hulpmiddelenzorg'],
            'Certain cancers': ['Inschrijftarieven', 'Farmaceutische zorg', 'Integrale kosten DBC-zorgproducten gereguleerde segment', 'Integrale kosten DBC-zorgproducten vrije segment', 'Add-ons dure geneesmiddelen', 'Fysiotherapie', 'Logopedie', 'NTS (en SKION t/m 2021)'],
            'High blood pressure': ['Inschrijftarieven', 'Consulten', 'Farmaceutische zorg', 'Eerstelijnsdiagnostiek', 'Multidisciplinaire zorg', 'Dieetadvisering', 'Gecombineerde leefstijlinterventies (GLI)'],

            # 4. Sleep and Recovery
            'Sleep apnea': ['Inschrijftarieven', 'Farmaceutische zorg', 'Consulten GGZ', 'Intramuraal verblijf GGZ', 'Eerstelijnsdiagnostiek', 'Integrale kosten DBC-zorgproducten gereguleerde segment', 'Integrale kosten DBC-zorgproducten vrije segment', 'Consulten', 'Avond-, nacht- en weekenddiensten', 'Hulpmiddelenzorg'],
            'Narcolepsy': ['Inschrijftarieven', 'Farmaceutische zorg', 'Consulten GGZ', 'Intramuraal verblijf GGZ', 'Eerstelijnsdiagnostiek', 'Consulten', 'Avond-, nacht- en weekenddiensten'],
            'Restless legs syndrome': ['Inschrijftarieven', 'Farmaceutische zorg', 'Consulten GGZ', 'Intramuraal verblijf GGZ', 'Eerstelijnsdiagnostiek', 'Consulten', 'Avond-, nacht- en weekenddiensten'],
            'Chronic Fatigue': ['Inschrijftarieven', 'Farmaceutische zorg', 'Consulten GGZ', 'Intramuraal verblijf GGZ', 'Eerstelijnsdiagnostiek', 'Fysiotherapie', 'Oefentherapie Mensendieck/Cesar', 'Ergotherapie', 'Consulten', 'Avond-, nacht- en weekenddiensten', 'Geneeskundige zorg specifieke patiëntgroepen (GZSP)'],

            # 5. Behavioural Change and Motivational Coaching
            'Prevented suicide': ['Inschrijftarieven', 'Vervoer per ambulance en helikopter', 'Farmaceutische zorg', 'Consulten GGZ', 'Intramuraal verblijf GGZ'],
            'Addiction': ['Inschrijftarieven', 'Vervoer per ambulance en helikopter', 'Farmaceutische zorg', 'Consulten GGZ','Intramuraal verblijf GGZ'],
            'Violence': ['Inschrijftarieven', 'Vervoer per ambulance en helikopter', 'Farmaceutische zorg', 'Consulten GGZ', 'Intramuraal verblijf GGZ'],
            'Abuse': ['Inschrijftarieven', 'Vervoer per ambulance en helikopter', 'Farmaceutische zorg', 'Consulten GGZ', 'Intramuraal verblijf GGZ']
        }

    def get_cost_per_condition(self, condition: str) -> tuple[float, str]:
        if condition not in self.condition_cost_mapping:
            debug_info = f"Warning: Condition '{condition}' not found in mapping."
            return 0.0, debug_info

        services = self.condition_cost_mapping[condition]
        total_cost = 0.0
        debug_info = f"Debug for {condition}:"
        
        for service in services:
            try:
                cost = self.df_costs.loc[service, self.COST_COLUMN].item()
                debug_info += f" {service}: {cost}"
                
                if isinstance(cost, (int, float)):
                    total_cost += cost
                else:
                    debug_info += f" (invalid type)"
                
            except KeyError:
                debug_info += f" {service}: NOT FOUND"
                debug_info += f" Available: {list(self.df_costs.index)}"
            except ValueError as e:
                debug_info += f" {service}: ERROR {e}"
        
        debug_info += f" Total: {total_cost}"
        return total_cost, debug_info
    

class ImpactTool:
    """Main tool for calculating healthcare impact"""
    
    CATEGORIES = {
        'Mental Health and Stress management': ['Burn-Out', 'Depression', 'Anxiety Disorder', 'Stress'],
        'Physical wellbeing and health': ['Hernia', 'RSI', 'Osteoarthritis', 'Cardiovascular diseases'],
        'Diet and lifestyle choices': ['Eating disorder', 'Type 2 diabetes', 'Certain cancers', 'High blood pressure'],
        'Sleep and recovery': ['Sleep apnea', 'Narcolepsy', 'Restless legs syndrome', 'Chronic Fatigue'],
        'Behavioural change and motivational coaching': ['Prevented suicide', 'Addiction', 'Violence', 'Abuse']
    }

    def __init__(self, cost_model: HealthcareCostModel):
        self.cost_model = cost_model
        self.patients_per_condition = {}
        self.total_patients_coach = 0
        self.results_df = None
        self.debug_info = []

    def calculate_impact(self, custom_costs=None):
        self.debug_info = []
        results = []
        total_societal_cost = 0.0

        for condition, count in self.patients_per_condition.items():
            if count > 0:
                if custom_costs and condition in custom_costs and custom_costs[condition] is not None:
                    cost_per_patient = custom_costs[condition]
                    debug_info = f"Debug for {condition}: Using custom cost € {cost_per_patient:,.2f}"
                else:
                    cost_per_patient, debug_info = self.cost_model.get_cost_per_condition(condition)
                
                self.debug_info.append(debug_info)
                total_cost = count * cost_per_patient
                total_societal_cost += total_cost
                
                results.append({
                    'Condition': condition,
                    'Patient_Count': count,
                    'Costs per patient': cost_per_patient,
                    'Total societal costs': total_cost
                })

        self.results_df = pd.DataFrame(results)
        self.total_societal_cost = total_societal_cost
