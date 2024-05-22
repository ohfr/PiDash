import GaugeComponent from 'react-gauge-component';
import { DashEvent } from '../types';

export default function Dash ({ events }: { events: DashEvent }) {
    return (
        <div
        style={{ display: 'flex', alignItems: 'center' }}> 
            <GaugeComponent
                minValue={0}
                maxValue={8000}
                style={{
                    width: '35%'
                }}
                labels={{
                    valueLabel: {
                        matchColorWithArc: true,
                        formatTextValue: (value: any) => `${value} RPM`
                    }
                }}
                arc={{
                    subArcs: [
                    {
                        limit: 5500,
                        color: '#5BE12C',
                    },
                    {
                        limit: 6500,
                        color: '#F58B19',
                    },
                    {
                        limit: 8000,
                        color: '#EA4228',
                    },
                    ]
                }}
                value={events.rpm}
            />
            <div>
                <GaugeComponent
                    minValue={0}
                    maxValue={40}
                    style={{
                        width: '80%'
                    }}
                    labels={{
                        valueLabel: {
                            matchColorWithArc: true,
                            formatTextValue: (value: any) => `${value} psi`
                        }
                    }}
                    arc={{
                        subArcs: [
                        {
                            limit: 25,
                            color: '#5BE12C',
                        },
                        {
                            limit: 35,
                            color: '#F58B19',
                        },
                        {
                            limit: 40,
                            color: '#EA4228',
                        },
                        ]
                    }}
                    value={events.boost}
                />
                <GaugeComponent
                    minValue={0}
                    maxValue={25}
                    style={{
                        width: '80%'
                    }}
                    labels={{
                        valueLabel: {
                            matchColorWithArc: true,
                            formatTextValue: (value: any) => `AFR ${value}`
                        }
                    }}
                    arc={{
                        subArcs: [
                        {
                            limit: 11,
                            color: '#EA4228',
                        },
                        {
                            limit: 16,
                            color: '#F58B19',
                        },
                        {
                            limit: 25,
                            color: '#5BE12C',
                        },
                        ]
                    }}
                    value={events.afr}
                />
                <GaugeComponent
                    minValue={0}
                    maxValue={260}
                    style={{
                        width: '80%'
                    }}
                    labels={{
                        valueLabel: {
                            matchColorWithArc: true,
                            formatTextValue: (value: any) => `coolant ${value}`
                        }
                    }}
                    arc={{
                        subArcs: [
                        {
                            limit: 215,
                            color: '#5BE12C',
                        },
                        {
                            limit: 230,
                            color: '#F58B19',
                        },
                        {
                            limit: 260,
                            color: '#EA4228',
                        },
                        ]
                    }}
                    value={events.coolant}
                />

                {/* <GaugeComponent
                    minValue={0}
                    maxValue={200}
                    labels={{
                        valueLabel: {
                            matchColorWithArc: true,
                            formatTextValue: (value: any) => `air temp ${value}`
                        }
                    }}
                    arc={{
                        subArcs: [
                        {
                            limit: 160,
                            color: '#5BE12C',
                        },
                        {
                            limit: 190,
                            color: '#F58B19',
                        },
                        {
                            limit: 200,
                            color: '#EA4228',
                        },
                        ]
                    }}
                    value={events.coolant}
                /> */}
            </div>
            <GaugeComponent
                minValue={0}
                maxValue={140}
                style={{
                    width: '35%'
                }}
                labels={{
                    valueLabel: {
                        matchColorWithArc: false,
                        style: { fill: '#FFFFFF', color: 'white', fontSize: 30},
                        formatTextValue: (value: any) => `${value} mph`
                    }
                }}
                arc={{
                    subArcs: [
                    {
                        limit: 0,
                        color: '#5BE12C',
                    },
                    {
                        limit: 10,
                        color: '#5BE12C',
                        showTick: true
                    },
                    {
                        limit: 20,
                        color: '#5BE12C',
                        showTick: true
                    },
                    {
                        limit: 30,
                        color: '#5BE12C',
                        showTick: true
                    },
                    {
                        limit: 40,
                        color: '#5BE12C',
                        showTick: true
                    },
                    {
                        limit: 50,
                        color: '#5BE12C',
                        showTick: true
                    },
                    {
                        limit: 60,
                        color: '#5BE12C',
                        showTick: true
                    },
                    {
                        limit: 70,
                        color: '#5BE12C',
                        showTick: true
                    },
                    {
                        limit: 80,
                        color: '#5BE12C',
                        showTick: true
                    },
                    {
                        limit: 90,
                        color: '#5BE12C',
                        showTick: true
                    },
                    {
                        limit: 100,
                        color: '#5BE12C',
                        showTick: true
                    },
                    {
                        limit: 110,
                        color: '#5BE12C',
                        showTick: true
                    },
                    {
                        limit: 120,
                        color: '#5BE12C',
                        showTick: true
                    },
                    {
                        limit: 130,
                        color: '#5BE12C',
                        showTick: true
                    },
                    {
                        limit: 140,
                        color: '#5BE12C',
                        showTick: true
                    },

                    ]
                }}
                value={events.speed}
            />
        </div>
    )
}